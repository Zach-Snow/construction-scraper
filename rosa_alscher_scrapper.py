import selenium
from time import sleep
from pprint import pprint
from selenium.webdriver.common.by import By
from datetime import datetime
from termcolor import colored
from database import db
from project_dict import project_dictionary


def rosa_scraper(browser):
    current_time = datetime.now().strftime('%d%m%Y')
    project_dict = project_dictionary
    project_dict["customer"] = "ROSA-ALSCHER Group"
    project_dict["scraping_date"] = current_time
    project_name_links = browser.find_elements(by=By.XPATH,
                                               value=f'.//div[@class="image_container"]')
    # pprint(project_name_links)
    raw_project_link_list = []
    return_list = []
    for item in project_name_links:
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
                                            value='.//*[@id="portfolio-details"]/div/div/h1').text
        project_location = browser.find_element(by=By.XPATH,
                                                value='.//*[@id="portfolio-details"]/div/div/h2').text
        table_rows = browser.find_elements(By.TAG_NAME, "tr")
        interim_value = ""
        for rows in table_rows:
            attribute_name = rows.find_elements(by=By.TAG_NAME, value="td")[0].text
            attribute_value = rows.find_elements(by=By.TAG_NAME, value="td")[1].text
            interim_value = f"{interim_value} {attribute_name} {attribute_value}"
        project_dictionary["project_location"] = project_location
        project_dictionary["project_name"] = project_name
        project_dictionary["link"] = link
        project_dictionary["project_information"] = interim_value
        database(action_bool=False, project_dictionary=project_dictionary)
        return_list.append(project_dictionary)
    return return_list


def database(action_bool: bool, project_dictionary: dict):
    # TODO: The pop has to be done to remove Duplicate ID error in pymongo
    try:
        project_dictionary.pop('_id')
    except KeyError:
        pass
    if not action_bool:
        rosa_alscher_db_data = db.rosa_alscher_projects.find_one(
            {"project_name": project_dictionary["project_name"],
             "project_location": project_dictionary["project_location"]},
            {"_id": False}
        )
        if not rosa_alscher_db_data:
            db.rosa_alscher_projects.insert_one(project_dictionary)
    elif action_bool and not project_dictionary:
        rosa_alscher_db_data = list(db.rosa_alscher_projects.find({}, {"_id": False}))
        return rosa_alscher_db_data
