#####
#####Written by: Tendai Makuwere
# Reviewed by Joao Claudio Macosso


# In this code we scrape app reviews, ratings and release date of popular apps on multiple devices
# the data is being scraped from https://www.commonsensemedia.org 
#Warning: these are not official reviews on respective platforms. unlike playstore and app store where 
#the user can only review apps that thety have used, this website does not have such restriction, 
#thus leading to questions regarding the quality of reviews. However, these reviews are usually made by professionals, hence reducing risks of spurious reviews
limit_page = True ## set to false to read all pages, else keep True to readonly first 100 pages


from datetime import datetime, timedelta
before = datetime.now()
current_time_1 = before.strftime("%H:%M:%S")
print("Current Time =", current_time_1)

from selenium import webdriver 
import selenium
from selenium import webdriver
import pandas as pd
import time
import csv
import sys, traceback
import re



if limit_page == True: 
    max_pages = 101
else: max_pages = 254

with open('Test.csv','w',encoding='utf-8') as file:  # creating a csv file
    file.write("App_Name, Age_Rating,Review,Date_Published, Platforms,link\n") #creating columns for scv file

webD=webdriver.Chrome(executable_path="C:\\webdrivers\\chromedriver.exe") #webdriver to run chrome
webD.get('https://www.commonsensemedia.org/app-reviews') # opening webpage
webD.maximize_window()
time.sleep(1)
cookie = webD.find_element_by_xpath('//*[@id="onetrust-pc-btn-handler"]').click() #accepting the cookie 
cookie2 =webD.find_element_by_xpath('//*[@id="onetrust-pc-sdk"]/div[3]/div[1]/button').click()#accepting terms and conditions of cookie
try:
    cookie.click() #clicking 
    time.sleep(5)
    cookie2.click()
except:
    pass

for k in range(4):
    titles =webD.find_elements_by_xpath('//div[@class="title-data-wrapper"]//strong//a') 
    #titles = titles.replace(',',' ')
    age = webD.find_elements_by_xpath("//div[@class = 'csm-green-age']")
    dates =webD.find_elements_by_xpath("//em[@class='field-content']//span[@datatype='xsd:dateTime']")
    d = [date.get_attribute('content') for date in dates]
    devices = webD.find_elements_by_xpath("//div[@class='views-field views-field-field-reference-review-ent-prod-field-term-app-platforms review-supplemental']//em[@class='field-content']")
    ratings = webD.find_elements_by_xpath("//span[@class='field-content']//div")
    c=[rate.get_attribute('class') for rate in ratings]
    links =webD.find_elements_by_xpath("//*[@id='content']/div/div/div[2]/div/div[4]/div/div/div[1]/div/div[2]/a")
    ls = [rate.get_attribute('href') for rate in links]
    
     

    with open('Test.csv','a',encoding='utf-8') as file:
        for i in range(len(titles)):
            file.write(re.sub(',','',titles[i].text) + "," + re.sub('\+','',re.sub('age ','',age[i].text)) +  ","+ c[i][26] + "," + d[i][:10] + "," + re.sub(',',';',devices[i].text )+","+ ls[i]+ "\n")

        next=webD.find_element_by_xpath("//a[@title='Go to next page']").click()
    file.close()
webD.close()

############
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time, ": Writing the output...")
############

############
now = datetime.now()
print("Current Time =", current_time, ": The full code is run, check the output in the directory...")
############

timeDif = now - before
print("Total time: ",str(timeDif.seconds), " Seconds")
