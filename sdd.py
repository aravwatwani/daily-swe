# software engineering daily digest. a script to notify users of new job postings.

from collections import defaultdict
from bs4 import BeautifulSoup as bs
import requests
# from selenium import webdriver
from twilio.rest import Client
import pandas as pd
from os import chdir
from glob import glob

# move to the path where CSV files are located
path = '/Users/aravwatwani/Desktop/projects/swe-daily-digest/'
chdir(path)
file_pattern = ".csv"
list_of_files = [file for file in glob('*.csv'.format(file_pattern))]


# prior data for checking if updates exist
old_data = pd.read_csv('data.csv')


data = defaultdict(list)
text_to_send = ''

try:
    url = 'https://github.com/pittcsc/Summer2022-Internships'
    r = requests.get(url)
    soup = bs(r.content, 'html.parser')
    table = soup.find('table')
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]

        if cols[0] not in data and cols[-1].lower() == 'closed':
            continue
        elif cols[0] not in data:
            data[cols[0]].extend(cols[1:])
        else:
            data[cols[0]] = cols[1:]
except:
   text_to_send = '🚨 Failed on bs4 execution'


data = pd.DataFrame(data).T
data.columns = ['Location', 'Role']
data.sort_index(inplace=True)
data.index.name = 'Company'
data



new_addition = False
# if len(data) > len(old_data):
#     new_addition = True

old_set = set([company for company in old_data['Company']])
new_set = set(data.index)
new_roles = list(old_set.symmetric_difference(new_set))
new_roles

# text_to_send = "Hello from Arav's bot 🤖 \n\n" 
# + 'Here are the latest software engineering internship openings for you!' 
# + '\n'.join(disclosures_clean) 
# + '\n\nThis script used to generate this message runs every Monday-Friday at 8:08AM PST. Cool.'


data.to_csv('data.csv')