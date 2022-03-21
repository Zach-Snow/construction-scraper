import selenium
from time import sleep
from pprint import pprint
from selenium.webdriver.common.by import By
from datetime import datetime
from termcolor import colored
from database import db
from project_dict import project_dictionary


# TODO: This one is a lot more complicated as there is no native data available for this companies portfolio
def brandberger_scraper(browser):
    current_time = datetime.now().strftime('%d%m%Y')
    current_containers = browser.find_elements(by=By.XPATH,
                                               value=f'.//div[@id="projects"]')
    for item in current_containers:
        project_information = item.find_elements(by=By.XPATH,
                                                 value='.//p[@class]')
        project_names = item.find_elements(by=By.TAG_NAME, value='h3')
        return_list = []

        # TODO: Remember, this has been done as the data is structured in a way that it is not possible to use the same dictionary for all project names.
        #  Each dictionary value has to be created separately to put in the same list.
        for project_name in project_names:
            project_dict = {"project_name": "",
                            "customer": "",
                            "project_information": "",
                            "scraping_date": ""}
            project_dict["customer"] = "BRAND BERGER GmbH & Co. KG"
            project_dict["scraping_date"] = current_time
            name = project_name.get_attribute('innerHTML')
            project_dict["project_name"] = name
            return_list.append(project_dict)
        project_info_counter = 0
        name_counter = 0
        list_length = len(project_information)
        # for value in return_list:
        while name_counter < list_length:
            interim_value = ""
            try:
                for i in range(name_counter, name_counter + 4):
                    raw_data = project_information[i].get_attribute('innerHTML')
                    class_name = project_information[i].get_attribute('class')
                    interim_value = f"{interim_value} {class_name}: {raw_data} "
                print("interim_value :", interim_value)
                return_list[name_counter-1]["project_information"] = interim_value
                project_info_counter = project_info_counter + 5
                name_counter = name_counter + 1
            except IndexError:
                return return_list
        return return_list
