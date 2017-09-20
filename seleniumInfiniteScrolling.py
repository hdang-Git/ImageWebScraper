# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 03:25:28 2017

@author: Hai
"""
from selenium import webdriver
import time

browser = webdriver.Firefox()

browser.get('https://www.google.com/search?q=watermelon&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjkka2_h7PWAhUKiVQKHfhJDvMQ_AUICigB&biw=1709&bih=940')
SCROLL_PAUSE_TIME = 0.5

# Get scroll height
last_height = browser.execute_script("return document.body.scrollHeight")

while True:
    # Scroll down to bottom
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = browser.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

html_source = browser.page_source
data = html_source.encode('utf-8')

with open('webpageSrc.html', 'wb') as f:
    f.write(data)
f.closed 


browser.quit()