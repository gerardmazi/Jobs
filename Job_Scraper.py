"""
JOB SCRAPER

@author:    Gerard Mazi
@date:      2020-03-06
@email:     gerard.mazi@gmail.com
@phone:     862-221-2477

"""

import pandas as pd
import numpy as np
from selenium import webdriver
import time
from datetime import date
import re

driver = webdriver.Chrome(r"chromedriver.exe")

time_stamp = pd.to_datetime('2020-04-09')

comps = 'https://www.linkedin.com/company/joinsquare/'

userid = 'gerard.mazi@gmail.com'
password = ''

driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
time.sleep(2)

# Login
driver.find_element_by_xpath('//*[@id="username"]').send_keys(userid)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
driver.find_element_by_xpath('//*[@class="btn__primary--large from__button--floating"]').click()
time.sleep(5)

# Run above first
#######################################################################################################################
# Go to company and jobs

driver.get(comps)
time.sleep(3)

# Navigate to jobs page
driver.find_element_by_xpath('//*[@data-control-name="page_member_main_nav_jobs_tab"]').click()
time.sleep(2)
driver.find_element_by_xpath('//*[@data-control-name="see_all_jobs"]').click()
time.sleep(2)

roles = list(
    map(
        int,
        re.findall(
            r'\d+(?:,\d+)?',
            driver.find_element_by_xpath('//*[@class="display-flex t-12 t-black--light t-normal"]').text
        )
    )
)[0]

pages = int(roles / 25)

role, company, location, info, descript = [], [], [], [], []

# Select role in left pane
driver.find_element_by_xpath('//*[@class="jobs-search-results__list artdeco-list"]/li[1]').click()

# Role Title
role = driver.find_element_by_xpath('//*[@class="jobs-details-top-card__job-title t-20 t-black t-normal"]').text

# Role location
loc = driver.find_element_by_xpath('//span[@class = "jobs-details-top-card__bullet"]').text

# Role description
desc = driver.find_element_by_xpath('//div[@class = "jobs-box__html-content jobs-description-content__text t-14 t-black--light t-normal"]').text

