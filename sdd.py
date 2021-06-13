# software engineering daily digest. a script to notify users of new job postings.

from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
from twilio.rest import Client

