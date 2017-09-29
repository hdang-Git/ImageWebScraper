# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 23:56:30 2017

@author: Hai


This program scrapes the preview images from google search and writes them 
to a file directory. It uses selenium to deal with the dynamic loading. 

In order to run, be sure to download the web drivers and add the path
of the web drivers to the system variables. Look at the Readme for more info.
"""

from bs4 import BeautifulSoup
import shutil
from selenium import webdriver
import time
from urllib.request import urlopen
import os
import errno

'''
Function uses selenium to scroll through the page until it reaches the full 
height of the web page and then gets the html page source.

@param urlPage - url of google image page
@param numImages - minimum number of images to get back
'''
def getBrowserSrcPage(urlPage, numImages): 
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
        foundImgNum = browser.find_elements_by_xpath("/html/body//img[@class='rg_ic rg_i']")
        print(len(foundImgNum))
        totalImagesFound = len(foundImgNum)
        
        if new_height == last_height:
            #check if total images found is greater than passed parameter 
            if totalImagesFound >= numImages:
                print('total images found: ' + str(totalImagesFound))
                break
            #else click on the 'show more results' button if there isn't enough images
            else:
#                if browser.find_element_by_xpath("/html/body//input[@id='smb']").size != 0:
#                    print('smb element size is 0')
#                    browser.find_element_by_xpath("/html/body//input[@id='smb']").click()
                
                
                 #EAFP principle
#                try:
#                    browser.find_element_by_xpath("/html/body//input[@id='smb']").click()
#                except:
#                    print('Element \'show more results\' not interactable thus not visible')
#                    print('max Elements: ' + str(totalImagesFound))
        last_height = new_height
        
    html_source = browser.page_source
    html_page = html_source.encode('utf-8')
    browser.quit()
    return html_page

'''
Function uses BeautifulSoup to look for the image tags and retrieves the 
image urls from the image tag's src attribute. 

@param html_page - stores html text for retrieved google image page
'''
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

'''
Function open the url links to retrieve the preview image data and then calls
writeImages() to write the image to the chosen directory.

@param imgLinks - stores retrieved urls of preview images
@param folderName - name of destination directory 
'''
def writeImagesToDir(imgLinks, folderName):
    #Write the image to file
    i = 0
    for imgUrl in imgLinks:
        fileName = folderName + '/' + str(i) + '.png'
        i += 1
        print(str(i) + '/' + str(len(imgLinks)))
        response = urlopen(imgUrl)
        writeImages(response, fileName)

'''
Function writes the data/bytes of the image to the output file.
 
@param response - stores image data
@param fileName - name of the file
'''
def writeImages(response, fileName):
    with open(fileName, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)
    del response
    
'''
Function creates a directory for images to be stored in.
 
@param directory - name of output folder
'''
def createDirectory(directory):
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except OSError as error:
            if error.errno != errno.EEXIST:
                raise

'''
Function controller which calls other functions to get the preview images 
from Google image search.
'''
def main():
    url = 'https://www.google.com/search?q=watermelon&source=lnms&tbm=isch&sa=X&ved=0ahUKEwjkka2_h7PWAhUKiVQKHfhJDvMQ_AUICigB&biw=1709&bih=940'
    outputFolderName = 'watermelon'
    htmlPage = getBrowserSrcPage(url, 1000);
#    imagesUrls = scrapeImages(htmlPage)
#    createDirectory(outputFolderName)
#    writeImagesToDir(imagesUrls, outputFolderName)
    print('Complete')
    
main()