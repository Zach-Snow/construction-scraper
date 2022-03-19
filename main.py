from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
import random

chrome_options = Options()
chrome_options.headless = False
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=chrome_options)


def garbe():
    url = "https://www.garbe-immobilien-projekte.de/projekte/"
    browser.get(url)
    project_name_link = browser.find_element(by=By.XPATH,
                                             value="/html/body/div[1]/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/div[2]/figure/a")
    project_name_link.click()


garbe()
