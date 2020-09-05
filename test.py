# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 16:46:05 2020

@author: chjhs
"""
import requests
from selenium import webdriver
import time
import random
from bs4 import BeautifulSoup
import csv

headerList = ['"title"','"period"','"register-due"','"place"','"link"','"content"']
with open('new_content.csv','w',newline='',encoding='utf-8-sig' )as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(("title","period","register-due","place","link","content"))
    csvfile.close()
    time.sleep(3)
options = webdriver.ChromeOptions()
options.add_argument('Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Mobile Safari/537.36')
#禁用图片提升爬取速度
prefs = {
              'profile.default_content_setting_values': {
                'images': 2,
                'javascript': 2        #2即为禁用的意思
                }
 }
options.add_experimental_option('prefs', prefs)
driver = webdriver.Chrome('./chromedriver.exe')

Skylinelinks=r'C:\Users\chjhs\Desktop\CrawlerForSkyline\Skylinelinks.csv'
headers={
        'Referer':'https://www.accupass.com/?area=north',
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Mobile Safari/537.36',
        }

total_list=[]
driver.get('https://skyline.tw/activity/activity-epa4mm0katcerxio9joyvitb29cg36r')
time.sleep(random.uniform(5,10))
htmltext = driver.page_source
    
    
# get the tilte for all the contest
soup = BeautifulSoup(htmltext,'lxml')

#contest-title
info_title = soup.find('div',class_='post-title')
info_TITLE=info_title.find('h2')
total_list.append(info_TITLE.text)
print(info_TITLE)
time.sleep(3)

#基本資訊(活動時間、報名時間、活動地點、官方連結)
general_info = soup.find('ul',class_='list list-lines')
general=general_info.find_all('li',limit=4)
for G in general:
    total_list.append(G.text)
    print(general)
time.sleep(3)
    
#活動內容
info_content = soup.find('div',class_='post-content-details')
total_list.append(info_content.text)
print(info_content)
time.sleep(3)

with open('new_content.csv','a',newline='',encoding='utf-8-sig' )as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(total_list)
    csvfile.close()
time.sleep(random.uniform(5,10))   