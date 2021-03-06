import selenium
from time import sleep
from pprint import pprint
from selenium.webdriver.common.by import By
from datetime import datetime
from termcolor import colored
from database import db


# TODO: Remember, the class name important now are: @data-category and @class="col-md-4".
def garbe_scraper(class_name: str,
                  browser):
    current_time = datetime.now().strftime('%d%m%Y')
    # use selenium chrome driver to fetch data related to projects
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
    return_list = []
    if class_name == '@class="col-md-4"':
        for link in final_link_list:
            # TODO:Structure dictionary to input in MongoDB database collection
            #  has to be made in the loop or only the last one is shown in the return_list.

            project_dict = {"project_name": "",
                            "project_location": "",
                            "customer": "GARBE Immobilien-Projekte",
                            "project_information": "",
                            "scraping_date": current_time,
                            "link": ""}
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
            project_dict["project_information"] = table
            project_dict["project_location"] = project_location
            project_dict["project_name"] = project_name
            project_dict["link"] = link
            return_list.append(project_dict)
            database(action_bool=False, project_dictionary=project_dict)

    elif class_name == "@data-category":
        for link in final_link_list:
            # TODO:Structure dictionary to input in MongoDB database collection
            #  has to be made in the loop or only the last one is shown in the return_list.
            project_dict = {"project_name": "",
                            "project_location": "",
                            "customer": "GARBE Immobilien-Projekte",
                            "project_information": "",
                            "scraping_date": current_time,
                            "link": ""}
            browser.get(link)
            project_location = browser.find_element(by=By.XPATH,
                                                    value='.//*[@id="main"]/div/div[3]/div/div[2]/header/h1').text
            project_name = browser.find_element(by=By.XPATH,
                                                value='.//*[@id="main"]/div/div[3]/div/div[2]/div/p').text
            table = browser.find_element(by=By.XPATH,
                                         value='.//*[@id="main"]/div/div[3]/div/div[3]/table').text
            project_dict["project_information"] = table
            project_dict["project_location"] = project_location
            project_dict["project_name"] = project_name
            project_dict["link"] = link
            return_list.append(project_dict)
            database(action_bool=False, project_dictionary=project_dict)

    return return_list


def database(action_bool: bool, project_dictionary: dict):
    # TODO: The pop has to be done to remove Duplicate ID error in pymongo
    try:
        project_dictionary.pop('_id')
    except KeyError:
        pass
    if not action_bool:
        garbe_db_data = db.garbe_projects.find_one(
            {"project_name": project_dictionary["project_name"],
             "project_location": project_dictionary["project_location"]},
            {"_id": False}
        )
        if not garbe_db_data:
            db.garbe_projects.insert_one(project_dictionary)
    elif action_bool and not project_dictionary:
        garbe_db_data = list(db.garbe_projects.find({}, {"_id": False}))
        return garbe_db_data
