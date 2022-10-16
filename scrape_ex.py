from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

options = Options()
options.headless = True
options.add_argument("--window-size=1920,1200")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.implicitly_wait(60)
driver.get('https://berkeleytime.com/catalog.html')

classes = set()

all_classes = driver.find_elements(By.CLASS_NAME, "filter-card-info")
for ind_class in all_classes:
    name = ind_class.find_element(By.TAG_NAME, "h6").text
    desc = ind_class.find_element(By.CLASS_NAME, "filter-card-info-desc").text

    classes.add((name, desc, ''))

# selenium scroll to bottom

print(classes)