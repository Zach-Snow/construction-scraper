import selenium
from time import sleep
from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
from termcolor import colored

chrome_options = Options()
chrome_options.headless = False
chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
browser = webdriver.Chrome(options=chrome_options)


def garbe():
    # step 1: Structure dictionary to input in MongoDB database collection
    current_time = datetime.now().strftime('%d%m%Y')
    project_dictionary = {"project_name": "",
                          "project_location": "",
                          "customer": "GARBE Immobilien-Projekte",
                          "project_information": "",
                          "scraping_date": current_time}

    # step 2: use selenium chrome driver to fetch data related to projects
    url = "https://www.garbe-immobilien-projekte.de/projekte/"
    browser.get(url)
    current_containers = browser.find_elements(by=By.XPATH,
                                               value='.//div[@class="col-md-4"]')
    raw_project_link_list = []
    for item in current_containers:
        project_name_links = item.find_elements(by=By.XPATH,
                                                value='.//a[@href]')
        for href in project_name_links:
            link = href.get_attribute("href")
            raw_project_link_list.append(link)

    final_link_list = list(set(raw_project_link_list))
    pprint(final_link_list)

    for link in final_link_list:
        browser.get(link)
        project_name = browser.find_element(by=By.XPATH,
                                            value="./html/body/div[1]/div[1]/div[2]/header/h1").text
        project_location = browser.find_element(by=By.XPATH,
                                                value="/html/body/div[1]/div[1]/div[2]/header/h2").text
        try:
            table = browser.find_element(by=By.XPATH,
                                         value="/html/body/div[1]/div[1]/div[5]/table").text
        except selenium.common.exceptions.NoSuchElementException:
            table = browser.find_element(by=By.XPATH,
                                         value="/html/body/div[1]/div[1]/div[5]/div/div[2]/div/table").text

        project_dictionary["project_information"] = table
        project_dictionary["project_location"] = project_location
        project_dictionary["project_name"] = project_name
        pprint(project_dictionary)
    browser.quit()

garbe()
