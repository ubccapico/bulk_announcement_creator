# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 11:34:47 2018

@author: Jeremy
"""
#Imports libraries that you need (automatic library install will only work with pip V.9,
#else you have to pip install libraries manually) 
from dateutil import parser
from datetime import datetime
from tqdm import tqdm
import pandas as pd
import re, pytz, getpass, requests

'''
Helpter function converts PDT time UTC time in preparation for Canvas API upload. 
Takes into consideration whether Daylight Savings is in effect.
@params:
    time_string: Tine in 24-hr PDT format (e.g. 9:30)
    boolean: Whether Daylight Savings is in effect
@return:
    String of time converted to UTC in form of T{hr}:{min}:00Z format
'''
def convert_pdt_utc(time_string, boolean):
    time_split = re.split(r"\:", time_string)
    time_hour_utc = int(time_split[0]) + 8

    if boolean:
        time_hour_utc -= 1

    if(time_hour_utc >= 24):
        time_hour_utc -= 24

    time_return = 'T{}:{}:00Z'.format(time_hour_utc, time_split[1])
    return time_return

'''
Main Function that runs announcement creator script on Canvas (Production). Will prompt user for
name of CSV (see format_example.csv for example), API token, and course ID. Will inform user
if request is successful or not.
@params:
    none
@returns:
    none
'''
if __name__ == "__main__":
    
    #Gets user parameters, file name, token, course ID.
    url = 'https://ubc.instructure.com'
    file_format = input('What file format (csv or xlsx)? ')
    name = input("Enter name of file: ")
    
    if file_format == 'csv':
        df = pd.read_csv('{}.csv'.format(name))
    else:
        df = pd.read_excel('{}.xlsx'.format(name))

    token = getpass.getpass("Enter Token: ")
    course_id = input("Enter Course ID: ")
 
    local = pytz.timezone ("America/Los_Angeles")

    print("Generating announcements...")
    with tqdm(total = len(list(df.iterrows()))) as pbar:
        for index, row in df.iterrows():
            pbar.update(1)
            #Parses values in CSV
            try:
                date = re.split(r"\/", row['date (m/d/y)'])
                date_time = str(row['date (m/d/y)']) + convert_pdt_utc(row['time'], bool(local.dst(datetime(int(date[2]), int(date[0]), int(date[1])), is_dst=None)))
                delay_time = parser.parse(date_time)
            except:
                print("Invalid date {}. Skipping announcement {}.".format(date_time, row['title']))
                continue
            
            #Sends request
            title = row['title']
            payload = {'title': title,
                       'message': row['message'],
                       'delayed_post_at': delay_time,
                       'is_announcement': True}

            r = requests.post(url + '/api/v1/courses/{}/discussion_topics'.format(course_id),
                              params = payload, headers={'Authorization': 'Bearer '+ token})
            if not r.ok:
                print("\n Failed to upload announcement, {} for {}.".format(title, delay_time))
