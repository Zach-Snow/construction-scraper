import selenium
from time import sleep
from pprint import pprint
from selenium.webdriver.common.by import By
from datetime import datetime
from termcolor import colored
from database import db

def brandberger_scraper():
    current_time = datetime.now().strftime('%d%m%Y')
    project_dictionary = {"project_name": "",
                          "project_location": "",
                          "customer": "ROSA-ALSCHER Group",
                          "project_information": "",
                          "scraping_date": current_time,
                          "link": ""}