from selenium import webdriver
from selenium.webdriver.chrome.options import Options


def set_driver(url: str):
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    return browser
