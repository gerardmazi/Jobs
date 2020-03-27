"""
JOB KEYWORD TREND

@author:    Gerard Mazi
@date:      2020-03-25
@email:     gerard.mazi@gmail.com
@phone:     862-221-2477

"""

import pandas as pd
import numpy as np
from selenium import webdriver
import time

comps = [
    'https://www.linkedin.com/company/joinsquare/',
    'https://www.linkedin.com/company/paypal/',
    'https://www.linkedin.com/company/the-trade-desk/',
    'https://www.linkedin.com/company/workday/',
    'https://www.linkedin.com/company/paycom/'
]

skills = [
    'data science', 'machine learning', 'artificial intelligence', 'deep learning', 'neural network', 'NLP',
    'distributed', 'natural language processing', 'computer vision'

    'python', 'hive', 'hadoop', 'spark', 'scala', 'tensorflow', 'kubernetes', 'SQL', 'ETL', 'tableau', 'PowerBI',
    'QuickSight', 'R', 'SAS', 'Redshift', "Snowflake", "S3", 'Presto', 'AWS', 'Azure', 'keras'
    
    'engineer', 'software', 'developer', 'api',

    'math', 'computer science', 'engineering', 'economics', 'statistics', 'physics', 'MS', 'masters', 'PhD'
    
    'blockchain', 'distributed ledger', 'cryptocurrency', 'bitcoin',

    'sales', 'customer success', 'account manager', 'engagement', 'implementation'
]

time_stamp = pd.to_datetime('2020-03-27')

int = pd.DataFrame({'Date': [], 'Comp': [], 'Info': [], 'FTE': [], 'Roles': [], 'Skill': [], 'Skill_No': []})

userid = ''
password = ''

driver = webdriver.Chrome(r"chromedriver.exe")

driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
time.sleep(2)

# Login
driver.find_element_by_xpath('//*[@id="username"]').send_keys(userid)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
driver.find_element_by_xpath('//*[@class="btn__primary--large from__button--floating"]').click()
time.sleep(3)

# Run above first
#######################################################################################################################
# Go to company and jobs
for c in comps:
    t_comp, t_info, t_fte, t_roles, = [], [], [], []

    driver.get(c)
    time.sleep(3)

    # Company name
    t_comp.append(
        driver.find_element_by_xpath('//*[@class="org-top-card-summary__title t-24 t-black truncate"]').text
    )

    # Company info
    t_info.append(
        driver.find_element_by_xpath('//*[@class="inline-block"]').text
    )

    # Full time employees
    t_fte.append(
        driver.find_element_by_xpath('//*[@data-control-name="topcard_see_all_employees"]').text
    )

    # Navigate to jobs page
    driver.find_element_by_xpath('//*[@data-control-name="page_member_main_nav_jobs_tab"]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@data-control-name="see_all_jobs"]').click()
    time.sleep(3)

    # Total number of jobs listed
    t_roles.append(
        driver.find_element_by_xpath('//*[@class="display-flex t-12 t-black--light t-normal"]').text
    )

    # Search pre-specified skills
    for s in skills:
        # Iterate through skills
        driver.find_element_by_xpath('//*[@class="jobs-search-box__text-input"]').clear()
        driver.find_element_by_xpath('//*[@class="jobs-search-box__text-input"]').send_keys(s)
        driver.find_element_by_css_selector('button.jobs-search-box__submit-button').click()
        time.sleep(3)

        # Apend results
        t_skills = []
        t_skills.append(
            driver.find_element_by_xpath('//*[@class="display-flex t-12 t-black--light t-normal"]').text
        )

        # Combine results
        temp = pd.DataFrame(
            {
                'Date':      time_stamp,
                'Comp':      t_comp,
                'Info':      t_info,
                'FTE':       t_fte,
                'Roles':     t_roles,
                'Skill':     [s],
                'Skill_No':  t_skills
            }
        )

        # Aggregate results
        int = pd.concat([int, temp], ignore_index=True)