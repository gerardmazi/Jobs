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

link = 'https://www.linkedin.com/jobs/search/?f_C=17719&locationId=OTHERS.worldwide'

driver.get(link)
driver.find_element_by_xpath('//li[@class = "occludable-update artdeco-list__item--offset-4 artdeco-list__item p0 ember-view"]').click()
driver.find_element_by_xpath('//h2[@class = "jobs-details-top-card__job-title t-20 t-black t-normal"]').text
driver.find_element_by_xpath('//a[@class = "jobs-details-top-card__company-url ember-view"]').text
driver.find_element_by_xpath('//a[@class = "jobs-details-top-card__exact-location t-black--light link-without-visited-state"]').text
driver.find_element_by_xpath('//ul[@class = "jobs-box__list jobs-description-details__list js-formatted-industries-list"]').text
driver.find_element_by_xpath('//div[@class = "jobs-box__html-content jobs-description-content__text t-14 t-black--light t-normal"]').text