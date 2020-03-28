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
from selenium.common.exceptions import NoSuchElementException
import time
import re


comps = [
    'https://www.linkedin.com/company/joinsquare/',
    'https://www.linkedin.com/company/paypal/'
]

data_sci = [
    'data science', 'machine learning', 'artificial intelligence', 'deep learning', 'neural networks', 'NLP',
    'distributed', 'natural language processing', 'computer vision'
]

tools = [
    'python', 'hive', 'hadoop', 'spark', 'scala', 'tensorflow', 'kubernetes', 'SQL', 'ETL', 'tableau', 'PowerBI',
    'QuickSight', 'R', 'SAS', 'Redshift', "Snowflake", "S3", 'Presto', 'AWS', 'Azure', 'keras'
]

dev = ['engineer', 'software', 'developer', 'api']

edu = ['math', 'computer science', 'engineering', 'economics', 'statistics', 'physics', 'MS', 'masters', 'PhD']

crypto = ['blockchain', 'distributed ledger', 'cryptocurrency', 'bitcoin']

sales = ['sales', 'customer success', 'account manager', 'engagement', 'implementation']

skills = data_sci + tools + dev + edu + crypto + sales

time_stamp = pd.to_datetime('2020-03-27')

jobs = pd.DataFrame({'Date': [], 'Comp': [], 'Info': [], 'FTE': [], 'Roles': [], 'Skill': [], 'Skill_No': []})

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

    driver.get(c)
    time.sleep(3)

    # Company name
    t_comp = driver.find_element_by_xpath('//*[@class="org-top-card-summary__title t-24 t-black truncate"]').text

    # LinkedIn followers
    t_info = re.findall(
        r'\d+(?:,\d+)?',
        driver.find_element_by_xpath('//*[@class="inline-block"]').text
    )

    # Full time employees
    t_fte = re.findall(
        r'\d+(?:,\d+)?',
        driver.find_element_by_xpath('//*[@data-control-name="topcard_see_all_employees"]').text
    )

    # Navigate to jobs page
    driver.find_element_by_xpath('//*[@data-control-name="page_member_main_nav_jobs_tab"]').click()
    time.sleep(3)
    driver.find_element_by_xpath('//*[@data-control-name="see_all_jobs"]').click()
    time.sleep(3)

    # Total number of jobs listed
    t_roles = re.findall(
        r'\d+(?:,\d+)?',
        driver.find_element_by_xpath('//*[@class="display-flex t-12 t-black--light t-normal"]').text
    )

    # Search pre-specified skills
    for s in skills:
        # Iterate through skills
        driver.find_element_by_xpath('//*[@class="jobs-search-box__text-input"]').clear()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@class="jobs-search-box__text-input"]').send_keys(s)
        driver.find_element_by_css_selector('button.jobs-search-box__submit-button').click()
        time.sleep(5)

        # Append results
        try:
            t_skills = re.findall(
                r'\d+(?:,\d+)?',
                driver.find_element_by_xpath('//*[@class="display-flex t-12 t-black--light t-normal"]').text
            )
        except NoSuchElementException:
            t_skills = '0'

        # Combine results - long format
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
        jobs = pd.concat([int, temp], ignore_index=True)
        time.sleep(2)

# Convert to integer
cols = ['Info', 'FTE', 'Roles', 'Skill_No']
for c in cols:
    jobs[c] = jobs[c].str.replace(',', '').astype(int)

# Job category
jobs['Cat'] = np.nan
jobs.loc[jobs.Skill.isin(data_sci), 'Cat'] = 'data_sci'
jobs.loc[jobs.Skill.isin(tools), 'Cat'] = 'tools'
jobs.loc[jobs.Skill.isin(dev), 'Cat'] = 'dev'
jobs.loc[jobs.Skill.isin(edu), 'Cat'] = 'edu'
jobs.loc[jobs.Skill.isin(crypto), 'Cat'] = 'crypto'
jobs.loc[jobs.Skill.isin(sales), 'Cat'] = 'sales'

# Append to stored jobs
job_store = pd.read_pickle('job_store.pkl')
job_store = pd.concat([job_store, jobs], axis=0)
job_store.to_pickle('job_store.pkl')

#######################################################################################################################
# ANALYTICS
pd.concat(
    [
        pd.crosstab(jobs.Comp, jobs.Cat, values=jobs.Skill_No, aggfunc=np.sum),
        pd.crosstab(jobs.Comp, jobs.Cat, values=jobs.Skill_No, normalize='index', aggfunc=np.sum)
    ]
)

job_trend = jobs.groupby(['Date', 'Comp', 'Cat'])['Skill_No'].sum().unstack()

job_trend['Total'] = job_trend.sum(axis=1)

job_trend = pd.merge(
    job_trend,
    jobs.groupby(['Date', 'Comp'])['Roles'].max(),
    how='left',
    on=['Date', 'Comp']
)

job_trend['Rel_Scor'] = job_trend.Roles / job_trend.Total

job_trend = pd.merge(
    job_trend,
    pd.crosstab(
        [jobs.Date, jobs.Comp],
        jobs.Cat,
        values=jobs.Skill_No,
        normalize='index',
        aggfunc=np.sum
    ),
    how='left',
    on=['Date', 'Comp'],
    suffixes=['', '_p']
)

