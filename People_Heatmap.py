"""
DISTRIBUTION OF PEOPLE ROLES

@author:    Gerard Mazi
@date:      2020-04-25
@email:     gerard.mazi@gmail.com
@phone:     862-221-2477

"""

import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import re

#roles = pd.read_pickle('store_roles.pkl')

'=============================================================='
comps = [
    'https://www.linkedin.com/company/anaplan/',
    'https://www.linkedin.com/company/blackline/',
    'https://www.linkedin.com/company/paypal/',
    'https://www.linkedin.com/company/joinsquare/',
    'https://www.linkedin.com/company/paycom/',
    'https://www.linkedin.com/company/crowdstrike/',
    'https://www.linkedin.com/company/qualys/',
    'https://www.linkedin.com/company/zscaler/',
    'https://www.linkedin.com/company/avalara/',
    'https://www.linkedin.com/company/fortinet/',
    'https://www.linkedin.com/company/okta-inc-/',
    'https://www.linkedin.com/company/palo-alto-networks/',
    'https://www.linkedin.com/company/servicenow/',
    'https://www.linkedin.com/company/tiny-spec-inc/',
    'https://www.linkedin.com/company/splunk/',
    'https://www.linkedin.com/company/twilio-inc-/',
    'https://www.linkedin.com/company/salesforce/',
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

time_stamp = pd.to_datetime('2020-04-24')

userid = 'gerard.mazi@gmail.com'
password = ''
'=============================================================='

role_temp = pd.DataFrame({'Date': [], 'Comp': [], 'Role': [], 'Count': []})

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

    # Navigate to people
    driver.find_element_by_xpath('//*[@data-control-name="page_member_main_nav_people_tab"]').click()
    time.sleep(2)

    # Show more drop down
    driver.find_element_by_xpath('//*[@data-control-name="people_toggle_see_more_insights_button"]').click()
    time.sleep(2)

    # Next Page
    driver.find_element_by_xpath('//*[@class="artdeco-carousel__navigation "]/div/button[2]').click()
    time.sleep(2)

    # Role
    driver.find_element_by_xpath('//*[@class="org-people-bar-graph-element__category"]').text
    time.sleep(2)
