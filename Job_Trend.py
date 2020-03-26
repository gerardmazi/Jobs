"""
JOB KEWORD TREND

@author:    Gerard Mazi
@date:      2020-03-25
@email:     gerard.mazi@gmail.com
@phone:     862-221-2477

"""

import pandas as pd
import numpy as np
from selenium import webdriver

userid = ''
password = ''

driver = webdriver.Chrome(r"chromedriver.exe")

driver.get('https://www.linkedin.com')

# Login
driver.find_element_by_xpath('//*[@class= nav__button-secondary"]').click()
driver.find_element_by_xpath('//*[@id="username"]').send_keys(userid)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
driver.find_element_by_xpath('//*[@class="btn__primary--large from__button--floating"]').click()

# Go to company and jobs
driver.get('https://www.linkedin.com/company/joinsquare/')
driver.find_element_by_xpath('//*[@class="inline-block"]').text
driver.find_element_by_xpath('//*[@class="v-align-middle"]').text
driver.find_element_by_xpath('//*[@data-control-name="page_member_main_nav_jobs_tab"]').click()
driver.find_element_by_xpath('//*[@data-control-name="see_all_jobs"]').click()

# Total job listings
driver.find_element_by_xpath('//*[@class="display-flex t-12 t-black--light t-normal"]').text

# Specific roles
driver.find_element_by_xpath('//*[@id="jobs-search-box-keyword-id-ember1990"]').send_keys('data science')
driver.find_element_by_css_selector('button.jobs-search-box__submit-button').click()
driver.find_element_by_xpath('//*[@class="display-flex t-12 t-black--light t-normal"]').text