![Image of Sauder](http://www.hec.ca/en/executive-education/news/2018/logo-UBC-Sauder.jpg)

# Bulk Announcement Creator
Creates a list of delayed announcements specified in a CSV or Excel file. Useful for when you need to create a large number of similar messages over a period of time. *Author(s): Jeremy H.*

## Instructions:
1. If you do not have Python, install it. If you have no experience with it, I recommend installing it through *https://www.anaconda.com/download/*.

2. Clone this GitHub repository.

3. Install all the dependencies using pip (first time use only). Use the command **pip install -r requirements.txt** through the command shell in the directory of your cloned git repo.

4. Open the *format_example.csv* to see how you need to format your CSV or Excel file to work with the script (file to be read by script must be in same directory as script). Each column is formatted in a specific fashion (column names have to be same as in *format_example.csv*):
    1. date(m/d/y) must be in mm/dd/yyyy format (e.g. 11/21/2018)
    2. message is written in HTML
    3. title is plain text
    4. time is in 24-hour format (e.g. 1:30 PM = 13:30)
    
5. Run the script. It will prompt you for your token, course id, and CSV/Excel file name.

