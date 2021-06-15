# software engineering daily digest. a script to notify users of new job postings.

from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from twilio.rest import Client

data = []
disclosures = []
text_to_send = ''
apple = False
apple_string = ''

# get list of URLs to visit and plunder!

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
        data.append({cols[0]: cols[-1]})
    # print(cols)

except:
   text_to_send = '🚨 Failed on bs4 execution'
   print(text_to_send)


print(data)