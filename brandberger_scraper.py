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
    project_dict = project_dictionary
    project_dict["customer"] = "BRAND BERGER GmbH & Co. KG"
    project_dict["scraping_date"] = current_time
    current_containers = browser.find_elements(by=By.XPATH,
                                               value=f'.//div[@id="projects"]')
    # final_link_list = list(set(project_name_links))
    pprint(current_containers)
    button = browser.find_element(value='//*[@id="projects"]/ul/li[2]/a')
    for item in current_containers:
        project_name_links = item.find_elements(by=By.XPATH,
                                                value='.//a[@href]')
        for href in project_name_links:
            link = href.get_attribute("href")
            print(link)
