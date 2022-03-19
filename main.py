from pprint import pprint

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random

chrome_options = Options()
chrome_options.headless = True
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=chrome_options)


def garbe():
    # step 1: Structure dictionary to input in MongoDB database collection
    project_dictionary = {"project_name": "",
                          "project_location": "",
                          "customer": "GARBE Immobilien-Projekte",
                          "project_information": ""}

    # step 2: use selenium chrome driver to fetch data related to projects
    url = "https://www.garbe-immobilien-projekte.de/projekte/"
    browser.get(url)
    project_name_link = browser.find_element(by=By.XPATH,
                                             value="/html/body/div[1]/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/div[2]/figure/a")
    project_name_link.click()
    project_name = browser.find_element(by=By.XPATH,
                                        value="/html/body/div[1]/div[1]/div[2]/header/h1").text
    project_location = browser.find_element(by=By.XPATH,
                                            value="/html/body/div[1]/div[1]/div[2]/header/h2").text
    table = browser.find_element(by=By.XPATH,
                                 value="/html/body/div[1]/div[1]/div[5]/table").text

    project_dictionary["project_information"] = table
    project_dictionary["project_location"] = project_location
    project_dictionary["project_name"] = project_name

    pprint(project_dictionary)


garbe()
