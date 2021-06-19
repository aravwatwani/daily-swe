# software engineering daily digest. a script to notify users of new job postings.

from collections import defaultdict
from bs4 import BeautifulSoup as bs
import requests
# from selenium import webdriver
from twilio.rest import Client

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



text_to_send = "Hello from Arav's bot 🤖 \n\n" 
+ 'Here are the latest software engineering internship openings for you!' 
+ '\n'.join(disclosures_clean) 
+ '\n\nThis script used to generate this message runs every Monday-Friday at 8:08AM PST. Cool.'

