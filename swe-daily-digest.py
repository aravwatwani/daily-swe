#!/usr/bin/env python
# coding: utf-8
# software engineering daily digest. a script to notify users of new job postings.

from collections import defaultdict
from bs4 import BeautifulSoup as bs
import requests
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
data.to_csv('new.csv')
new_data = pd.read_csv('new.csv')

new_addition = False
all_new_roles = []
for index, company in enumerate(new_data['Company']):
    if company not in list(old_data['Company']):
        new_addition = True
        if str(new_data['Role'][index]) == 'nan':
            all_new_roles.append("Openings at " + company)
        else:
            all_new_roles.append(new_data['Role'][index] + " at " + company)

if not new_addition:
    exit()

new_data.to_csv('data.csv')
text_to_send = "Hello from Arav's bot 🤖\n\n" + 'Here are the latest software engineering internship openings for you! \n\n' + '\n'.join(all_new_roles) + '\n\nThis script used to generate this message runs every day at 8:00 AM PST.'

account_sid = "[redacted]"
auth_token = "[redacted]"
try:
   client = Client(account_sid, auth_token)
   message = client.messages.create(body=text_to_send, to='+[redacted]', from_='+[redacted]')
except:
   print('🚨 Error connecting to Twilio client')

