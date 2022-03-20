import selenium
from time import sleep
from pprint import pprint
from selenium.webdriver.common.by import By
from datetime import datetime
from termcolor import colored
from database import db
from project_dict import project_dictionary


# TODO: Remember, the class name important now are: @data-category and @class="col-md-4".
def garbe_scraper(class_name: str,
                  browser):
    # step 1: Structure dictionary to input in MongoDB database collection
    current_time = datetime.now().strftime('%d%m%Y')
    project_dict = project_dictionary
    project_dict["customer"] = "GARBE Immobilien-Projekte"
    project_dict["scraping_date"] = current_time

    # step 2: use selenium chrome driver to fetch data related to projects
    current_containers = browser.find_elements(by=By.XPATH,
                                               value=f'.//div[{class_name}]')
    raw_project_link_list = []
    for item in current_containers:
        project_name_links = item.find_elements(by=By.XPATH,
                                                value='.//a[@href]')
        for href in project_name_links:
            link = href.get_attribute("href")
            raw_project_link_list.append(link)

    final_link_list = list(set(raw_project_link_list))
    pprint(final_link_list)
    return_list = []
    if class_name == '@class="col-md-4"':
        for link in final_link_list:
            browser.get(link)
            project_name = browser.find_element(by=By.XPATH,
                                                value='.//*[@id="open"]/div[2]/header/h1').text
            project_location = browser.find_element(by=By.XPATH,
                                                    value='.//*[@id="open"]/div[2]/header/h2').text
            try:
                table = browser.find_element(by=By.XPATH,
                                             value='.//*[@id="open"]/div[5]/table').text
            except selenium.common.exceptions.NoSuchElementException:
                table = browser.find_element(by=By.XPATH,
                                             value='.//*[@id="open"]/div[5]/div/div[2]/div/table').text
            project_dictionary["project_information"] = table
            project_dictionary["project_location"] = project_location
            project_dictionary["project_name"] = project_name
            project_dictionary["link"] = link
            return_list.append(project_dictionary)
            pprint(project_dictionary)
    elif class_name == "@data-category":
        for link in final_link_list:
            browser.get(link)
            project_location = browser.find_element(by=By.XPATH,
                                                    value='.//*[@id="main"]/div/div[3]/div/div[2]/header/h1').text
            project_name = browser.find_element(by=By.XPATH,
                                                value='.//*[@id="main"]/div/div[3]/div/div[2]/div/p').text
            table = browser.find_element(by=By.XPATH,
                                         value='.//*[@id="main"]/div/div[3]/div/div[3]/table').text
            project_dictionary["project_information"] = table
            project_dictionary["project_location"] = project_location
            project_dictionary["project_name"] = project_name
            project_dictionary["link"] = link
            return_list.append(project_dictionary)
            pprint(project_dictionary)

    return return_list
