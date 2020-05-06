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

jobs = pd.read_pickle('store_jobs.pkl')

'=============================================================='
comps = [
    'https://www.linkedin.com/company/atlassian/',
    'https://www.linkedin.com/company/box/',
    'https://www.linkedin.com/company/docusign/',
    'https://www.linkedin.com/company/ringcentral/',
    'https://www.linkedin.com/company/smartsheet-com/',
    'https://www.linkedin.com/company/coupa-software/',
    'https://www.linkedin.com/company/dropbox/',
    'https://www.linkedin.com/company/five9/',
    'https://www.linkedin.com/company/redfin/',
    'https://www.linkedin.com/company/zillow/',
    'https://www.linkedin.com/company/veeva-systems/',
    'https://www.linkedin.com/company/appfolio-inc/',
    'https://www.linkedin.com/company/upland-software/',
    'https://www.linkedin.com/company/zuora/'
]

time_stamp = pd.to_datetime('2020-05-06')

userid = 'gerard.mazi@gmail.com'
password = ''
'=============================================================='

data_sci = ['machine learning', 'deep learning', 'neural networks', 'NLP', 'natural language processing']

tools = ['python']

dev = ['engineer']

edu = ['computer science', 'PhD']

crypto = ['blockchain', 'distributed ledger']

sales = ['sales', 'customer success', 'account manager', 'consultant']

skills = data_sci + dev + edu + crypto + sales

job_temp = pd.DataFrame({'Date': [], 'Comp': [], 'Info': [], 'FTE': [], 'Roles': [], 'Skill': [], 'Skill_No': []})

driver = webdriver.Chrome(r"chromedriver.exe")

driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
time.sleep(2)

# Login
driver.find_element_by_xpath('//*[@id="username"]').send_keys(userid)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
driver.find_element_by_xpath('//*[@class="btn__primary--large from__button--floating"]').click()

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
    time.sleep(2)
    driver.find_element_by_xpath('//*[@data-control-name="see_all_jobs"]').click()
    time.sleep(2)

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
        time.sleep(1)
        driver.find_element_by_css_selector('button.jobs-search-box__submit-button').click()
        time.sleep(3)

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
        job_temp = pd.concat([job_temp, temp], ignore_index=True)
        time.sleep(2)

#######################################################################################################################
# Convert to integer
cols = ['Info', 'FTE', 'Roles', 'Skill_No']
for c in cols:
    job_temp[c] = job_temp[c].str.replace(',', '').astype(int)

# Job category
job_temp['Cat'] = np.nan
job_temp.loc[job_temp.Skill.isin(data_sci), 'Cat'] = 'data_sci'
job_temp.loc[job_temp.Skill.isin(tools), 'Cat'] = 'tools'
job_temp.loc[job_temp.Skill.isin(dev), 'Cat'] = 'dev'
job_temp.loc[job_temp.Skill.isin(edu), 'Cat'] = 'edu'
job_temp.loc[job_temp.Skill.isin(crypto), 'Cat'] = 'crypto'
job_temp.loc[job_temp.Skill.isin(sales), 'Cat'] = 'sales'

# Append to stored jobs
jobs = pd.concat([jobs, job_temp], axis=0, ignore_index=True)
jobs.to_pickle('store_jobs.pkl')

#######################################################################################################################
# ANALYTICS
pd.concat(
    [
        pd.crosstab(job_temp.Comp, job_temp.Cat, values=job_temp.Skill_No, aggfunc=np.mean),
        pd.crosstab(job_temp.Comp, job_temp.Cat, values=job_temp.Skill_No, normalize='index', aggfunc=np.mean)
    ]
)

# Initial trend data frame
job_trend = jobs.groupby(['Date', 'Comp', 'Cat'])['Skill_No'].sum().unstack().reset_index()

# Total roles scraped
job_trend['Total'] = job_trend.sum(axis=1)

# Merge posted roles
job_trend = pd.merge(
    job_trend,
    jobs.groupby(['Date', 'Comp'])['Roles'].max().reset_index(),
    how='left',
    on=['Date', 'Comp']
)

# Merge in number of employees
job_trend = pd.merge(
    job_trend,
    jobs.groupby(['Date', 'Comp'])['FTE'].max().reset_index(),
    how='left',
    on=['Date', 'Comp']
)

# Reliability Score (can we trust the results) (higher better)
job_trend['Rel_Scor'] = job_trend.Roles / job_trend.Total

# Roles per employee (high => hiring)
job_trend['Hiring'] = job_trend.Roles / job_trend.FTE

# Merge in the proportional (_p) role distributions
job_trend = pd.merge(
    job_trend,
    pd.crosstab(
        [jobs.Date, jobs.Comp],
        jobs.Cat,
        values=jobs.Skill_No,
        normalize='index',
        aggfunc=np.sum
    ).reset_index(),
    how='left',
    on=['Date', 'Comp'],
    suffixes=['', '_p']
)

job_trend.to_csv('out_job_trend.csv')

# Individual comps
comp_trend = job_trend.loc[job_trend.Comp == 'Zendesk', ['Date', 'FTE', 'Roles']].set_index('Date')
comp_trend['Roles'].plot(title='Open Roles')
comp_trend['FTE'].plot(title='Total FTEs')