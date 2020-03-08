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

driver = webdriver.Chrome(r"chromedriver.exe")

driver.get('https://www.linkedin.com/jobs/search/?f_C=37759&locationId=OTHERS.worldwide')

roles = int(driver.find_element_by_xpath('//span[@class = "results-context-header__job-count"]').text)
pages = int(roles / 25)

role, company, location, info, descript = [], [], [], [], []

for p in range(pages):
    driver.find_element_by_xpath('//button[@class = "see-more-jobs"]').click()
    print('trial ' + str(p))
    time.sleep(2)

for r in range(roles):
    # Select listing
    driver.find_element_by_xpath('//a[@class = "result-card__full-card-link"]').click()

    # Record role
    role_nam = driver.find_element_by_xpath('//h2[@class = "topcard__title"]').text
    role.append(role_nam)

    # Record company name
    comp_nam = driver.find_element_by_xpath('//a[@class = "topcard__org-name-link topcard__flavor--black-link"]').text
    company.append(comp_nam)

    # Record location
    loc_nam = driver.find_element_by_xpath('//span[@class = "topcard__flavor topcard__flavor--bullet"]').text
    location.append(loc_nam)

    # Additional role info
    add_info = driver.find_element_by_xpath('//ul[@class = "job-criteria__list"]').text
    info.append(add_info)

    # Role description
    role_desc = driver.find_element_by_xpath('//div[@class = "description__text description__text--rich"]').text
    descript.append(role_desc)

