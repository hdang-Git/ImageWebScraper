# -*- coding: utf-8 -*-
"""
Created on Tue Sep 19 23:48:15 2017

@author: Hai
"""

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()

browser.get('http://www.yahoo.com')
assert 'Yahoo' in browser.title

elem = browser.find_element_by_name('p')  # Find the search box
elem.send_keys('seleniumhq' + Keys.RETURN)


browser.quit()