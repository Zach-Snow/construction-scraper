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
new_browser = webdriver.Chrome(options=chrome_options)


def garbe_sort_link(class_name: str):
    url = "https://www.garbe-immobilien-projekte.de/projekte/"
    new_browser.get(url)
    current_containers = new_browser.find_elements(by=By.XPATH,
                                                   value=f'.//div[@class={class_name}]')
    raw_project_link_list = []
    final_link_list = []
    try:
        for item in current_containers:
            project_name_links = item.find_elements(by=By.XPATH,
                                                    value='.//a[@href]')
            for href in project_name_links:
                link = href.get_attribute("href")
                raw_project_link_list.append(link)
        print(raw_project_link_list)
        final_link_list = list(set(raw_project_link_list))
    except selenium.common.exceptions.NoSuchElementException:
        print(colored("Website has been updated for getting the list of current projects! Update the Scraper!", "red"))
    new_browser.quit()
    pprint(final_link_list)
    return final_link_list




 # step 3: Get information for previously finished project data
    # try:
    # browser.get(url)
    # previous_projects = browser.find_elements(by=By.XPATH,
    #                                           value='.//div[@data-category]')
    # raw_old_projects = []
    # for old_project in previous_projects:
    #     old_project_name_links = old_project.find_elements(by=By.XPATH,
    #                                                        value='.//a[@href]')
    #     for n_href in old_project_name_links:
    #         link = n_href.get_attribute("href")
    #         raw_old_projects.append(link)
    # pprint(raw_old_projects)
    # old_project.click()
    # # try:
    # sleep(2)
    # nproject_name = browser.find_element(by=By.XPATH,
    #                                      value='.//*[@id="main"]/div/div[3]/div/div[2]/header/h1').text
    # print(nproject_name)
    # nproject_location = browser.find_element(by=By.XPATH,
    #                                          value='.//*[@id="main"]/div/div[3]/div/div[2]/div/p').text
    # print(nproject_location)
    # ntable = browser.find_element(by=By.XPATH,
    #                               value='.//*[@id="main"]/div/div[3]/div/div[3]/table').text
    # print(ntable)
    # except selenium.common.exceptions.NoSuchElementException:
    #     print("data not found 2nd!")
    # project_dictionary["project_information"] = table
    # project_dictionary["project_location"] = project_location
    # project_dictionary["project_name"] = project_name
    # pprint(project_dictionary)
    # except:
    #     pass
