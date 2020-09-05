import requests
from selenium import webdriver
import time
import random
from bs4 import BeautifulSoup
import csv

#---------------------------------------------------開啟 CromeDriver------------------------------------------------------------------------

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


#------------------------------------爬搜尋頁(skyline為例)並將連結存在 csv 檔裡 -----------------------------------------------------------------------------
Skylinelinks=r'C:\Users\chjhs\Desktop\CrawlerForSkyline\Skylinelinks.csv' #請改成自己的絕對路徑
link_list=[]
for page in range(1,15,1):
    driver.get('https://skyline.tw/activity/explore?category=10&region=&price=&duration=&time_filter=created_at_desc&page='+str(page))
    headers={
        'Referer':'https://www.accupass.com/?area=north',
        'User-Agent':'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Mobile Safari/537.36',
    }
    
    time.sleep(random.uniform(5,10))
    soup = BeautifulSoup(driver.page_source, "html.parser")
    
    a_tag=soup.select('div.post-title a')
    for link in a_tag:
        data = link.get('href')
        link_list.append(data)
        print(data)
    time.sleep(random.uniform(5,10))
    
data_length=len(data)
print(data_length)
    

    
#爬到的連結存入csv檔    
with open('Skylinelinks.csv','w',newline='',encoding='utf-8-sig' )as csvfile:
        writer=csv.writer(csvfile)
        writer.writerow(link_list)
        csvfile.close()
        time.sleep(random.uniform(5,10))
        
        
        
#-----------------------------------------從資料夾讀取連結再一個一個爬--------------------------------

#設定表頭
headerList = ['title','period','register-due','place','link','content']
with open('content.csv','w',newline='',encoding='utf-8-sig' )as csvfile:
    writer=csv.writer(csvfile)
    writer.writerow(headerList)
    csvfile.close()
    time.sleep(3)

#用迴圈去csv檔一個一個打開連接再將活動資訊爬下來
for win in range(data_length):
    total_list=[]
    f = open(Skylinelinks, 'r',encoding='UTF-8-sig')
    csvreader = csv.reader(f)
    run_rows = [row[win] for row in csvreader]
    print(run_rows)
    url=str(run_rows).replace('[','').replace(']','').replace("'","")
    print(url)
    driver.get(url)
    time.sleep(random.uniform(5,10))
    htmltext = driver.page_source
    
    
    # get the tilte for all the contest
    soup = BeautifulSoup(htmltext,'lxml')

    #contest-title
    info_title = soup.find('div',class_='post-title')
    info_TITLE=info_title.find('h2')
    total_list.append(info_TITLE.text)
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
    time.sleep(3)
    
    # total_list.append(info_title.text,info_period.text,info_appartment.text,limit_1.text,info_content.text)

    #寫入csv
    with open('content.csv','a',newline='',encoding='utf-8-sig' )as csvfile:
        writer=csv.writer(csvfile)
        writer.writerow(total_list)
        csvfile.close()
    time.sleep(random.uniform(5,10))   
