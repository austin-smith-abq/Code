#selenium4
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import time


options = Options()
options.headless = False

driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()),options=options)


url = "https://www.sbnm.org/cvweb/cgi-bin/utilities.dll/openpage?wrp=membersearch.htm"
options.headless = True
driver.get(url)

time.sleep(10)

with open('sbnm.txt', 'w') as f:
    f.write(driver.page_source)

driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/form/fieldset/div[13]/div/button[1]').click()

# Read every csv in bar_association\bar_association\Results
# import csv
# import os
# import glob
#
# os.chdir("./Results")
# for file in glob.glob("*.csv"):
#     with open(file, 'r') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             print(row)

