"""
GeekWire 200 Ranking Trends

@author:    Gerard Mazi
@date:      2020-05-04
@email:     gerard.mazi@gmail.com
@phone:     862-221-2477

"""

import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import re

GeekWire200 = pd.read_pickle('store_GeekWire200.pkl')

time_stamp = pd.to_datetime('2020-05-04')


driver = webdriver.Chrome(r"chromedriver.exe")

driver.get('https://www.geekwire.com/geekwire-200/')

t_Rank, t_Comp, t_Cat, t_twtr, t_fb, t_linkFTE, t_linkF = [], [], [], [], [], [], []

for i in range(1, 201):

    t_Rank.append(
        driver.find_element_by_xpath('//*[@class="table table-striped dataTable no-footer"]/tbody/tr[' + str(i) + ']/td[1]').text
    )

    t_Comp.append(
        driver.find_element_by_xpath('//*[@class="table table-striped dataTable no-footer"]/tbody/tr[' + str(i) + ']/td[2]/div[2]/div[1]').text
    )

    t_Cat.append(
        driver.find_element_by_xpath('//*[@class="table table-striped dataTable no-footer"]/tbody/tr[' + str(i) + ']/td[2]/div[2]/div[2]').text
    )

    t_twtr.append(
        driver.find_element_by_xpath('//*[@class="table table-striped dataTable no-footer"]/tbody/tr[' + str(i) + ']/td[3]').text
    )

    t_fb.append(
        driver.find_element_by_xpath('//*[@class="table table-striped dataTable no-footer"]/tbody/tr[' + str(i) + ']/td[4]').text
    )

    t_linkFTE.append(
        driver.find_element_by_xpath('//*[@class="table table-striped dataTable no-footer"]/tbody/tr[' + str(i) + ']/td[5]').text
    )

    t_linkF.append(
        driver.find_element_by_xpath('//*[@class="table table-striped dataTable no-footer"]/tbody/tr[' + str(i) + ']/td[6]').text
    )

    temp = pd.DataFrame(
        {
            'Date': time_stamp,
            'Rank': t_Rank,
            'Comp': t_Comp,
            'Cat': t_Cat,
            'Twitter_Followers': t_twtr,
            'Facebook_Likes': t_fb,
            'Linkedin_Employees': t_linkFTE,
            'Linkedin_Followers': t_linkF
        }
    )

GeekWire200 = pd.concat([GeekWire200, temp], ignore_index=True)

GeekWire200.to_pickle('store_GeekWire200.pkl')