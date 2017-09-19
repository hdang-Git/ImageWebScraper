# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 22:49:54 2017

@author: Hai
"""
from bs4 import BeautifulSoup
import requests
import shutil

#urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
url = 'https://www.google.com/search?q=apple&tbm=isch&source=lnms&sa=X&ved=0ahUKEwj75oiJ-K3WAhVLhlQKHUJHALMQ_AUICygC&biw=1709&bih=940&dpr=1'

r = requests.get(url)
print(r.url)
#print(r.text)
html_page = r.text
soup = BeautifulSoup(html_page,'html.parser')


imgLinks = []

containers = soup.find(id="ires")
table = containers.table.find_all('tr')

for row in table:       #rows hold <tr> tag
    for cell in row:        #cell holds <td> tag
        if(cell != None):
            print(cell.a.img['src'])
            imgLinks.append(cell.a.img['src'])
    
print(len(imgLinks))


i = 0
for imgUrl in imgLinks:
    fileName = str(i) + '.png'
    i += 1
    response = requests.get(imgUrl, stream=True)
    with open(fileName, 'wb') as out_file:
        shutil.copyfileobj(response.raw, out_file)
    del response
