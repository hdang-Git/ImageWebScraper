# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 23:56:30 2017

@author: Hai


This program scrapes the preview images from google search and writes them 
to a file directory, using selenium to deal with the dynamic loading. 
"""

# id="rg_s"  div
#class="rg_bx rg_di rg_el ivg-i"   div a img 

from bs4 import BeautifulSoup
import requests
import shutil
from selenium import webdriver
import time
from urllib.request import urlopen
import os
import errno

def getBrowserSrcPage(urlPage): 
    browser = webdriver.Firefox()
    browser.get(urlPage)
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
    html_page = html_source.encode('utf-8')
    browser.quit()
    return html_page

def scrapeImages(html_page):
    #Parse the google page for the image links
    imgLinks = []
    soup = BeautifulSoup(html_page,'html.parser')
    #TODO: consider dfr-src or data-src in future reference
    imageLinks = soup.find_all('img', {"src":True}, {'class': 'rg_ic rg_i'})
    j = 0
    for link in imageLinks:
        print(j)
        j += 1
        print(link['src'])
        #check if valid url; google has certain images that are stored locally 
        #their server which can't be accessed 
        if(not link['src'].startswith('/')):
            imgLinks.append(link['src'])
        else:
            print('Not a valid url.') 
    print(len(imgLinks))
    return imgLinks

def writeImagesToDir(imgLinks, folderName):
    #Write the image to file
    i = 0
    for imgUrl in imgLinks:
        fileName = folderName + '/' + str(i) + '.png'
        i += 1
        print(i)
        if imgUrl.startswith('data:image/jpeg;base64') or imgUrl.startswith('data:image/png;base64'):
            response = urlopen(imgUrl)
            writeImages(response, fileName)
        else: 
            response = requests.get(imgUrl.strip(), stream=True)
            writeImages(response.raw, fileName)

def writeImages(response, fileName):
    with open(fileName, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    del response
    
def createDirectory(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as error:
            if error.errno != errno.EEXIST:
                raise
    
def main():
    url = 'https://www.google.com/search?q=watermelon&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjkka2_h7PWAhUKiVQKHfhJDvMQ_AUICigB&biw=1709&bih=940'
    outputFolderName = 'watermelon'
    htmlPage = getBrowserSrcPage(url);
    imagesUrls = scrapeImages(htmlPage)
    createDirectory(outputFolderName)
    writeImagesToDir(imagesUrls, outputFolderName)
    
main()