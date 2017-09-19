# -*- coding: utf-8 -*-
"""
Created on Sun Sep 17 22:31:39 2017

@author: Hai
"""

import urllib3

http = urllib3.PoolManager()
r = http.request('GET', 'http://httpbin.org/robots.txt')
r.status 
print(r.status)