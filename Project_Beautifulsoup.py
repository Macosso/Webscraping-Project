#####Written by: Joao Claudio Macosso
limit_page = True ## set to false to read all pages, else keep True to readonly first 100 pages
#####
# In this code we scrape app reviews, ratings and release date of popular apps on multiple devices
# the data is being scraped from https://www.commonsensemedia.org 
#Warning: these are not official reviews on respective platforms. unlike playstore and app store where 
#the user can only review apps that thety have used, this website does not have such restriction, 
#thus leading to questions regarding the quality of reviews. However, these reviews are usually made by professionals, hence reducing risks of spurious reviews
from datetime import datetime, timedelta
before = datetime.now()
current_time_1 = before.strftime("%H:%M:%S")
print("Current Time =", current_time_1)


from datetime import datetime
from bs4 import BeautifulSoup as BS
import pandas as pd
import re
import requests
import os
os.chdir("C:\\Users\\User\\Google Drive\\UW WNE\\Semester 4\\Webscraping\\Project")  # set the directory if you'll need to save files
import lxml

if limit_page == True:
    max_pages = 101
else:
    max_pages = 254
    
############
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time, ": Extracting links")
############

# domain = "https://www.commonsensemedia.org"
# url = "https://www.commonsensemedia.org/app-reviews"
# html = requests.get(url)
# bs = BS(html.text)

domain = "https://www.commonsensemedia.org"

###it was spotted that all the pages are following a certain patern 
#first page is "https://www.commonsensemedia.org/app-reviews"
# the next pages "https://www.commonsensemedia.org/app-reviews" + ?page=i" i takes values from 1 to 243
# therefore a list was created containing these links
links=["https://www.commonsensemedia.org/app-reviews"] #starting a link with the first page in which I will append the next pages
for i in range(1,244): #set the number of pages that will be scraped, the maximum number is 243 pages
    links.append("https://www.commonsensemedia.org/app-reviews"+ "?page="+str(i))


dta = pd.DataFrame({"App_Name": [], "Date_Published":[], "Platforms":[], "Review":[], "Link":[], "Age_Rating":[]})



############
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time, ": Scraping the data, this may take about 8 minutes, be patient...")
############


    
for url in links:
    html = requests.get(url)
    bs = BS(html.text, features="lxml")
    apps = bs.find_all('div', {'class':"content-content-wrapper"})
    
    for app in apps:
        try:
           App_Name = app.find('div', {'class':"views-field views-field-field-reference-review-ent-prod result-title"}).text[1:-1] #need to trim the first character and last as they are blank and makes difficult when filtering
           App_Name = re.sub(',','',App_Name) #remove commas in the name
        except:
            App_Name = ""
        
        try:
            Review = app.find('div', {'class': "views-field views-field-field-stars-rating inline rating-value"}).find('div')['class'][2][-1] #filtering only the numeric par which goes from 1 to 5
                
        except:
            Review =""
        
        try:
            Platforms = bs.find('em', {'class':"field-content"}).text
            Platforms = re.sub(",", ";",Platforms)
        except:
            Platforms = ""
        
        try:
            Link = domain + app.find('div', {'class':"views-field views-field-field-reference-review-ent-prod result-title"}).find('strong', {'class':"field-content"}).find('a')['href']
        except:
            Link = ""
        
        try:
            Date_Published = app.find('span', {'class':"date-display-single"})['content'][0:10]
        except:
            Date_Published = ""
        
        try:
            Age_Rating = app.find('div', {'class': 'csm-green-age'}).text
            Age_Rating = re.sub("age ","", Age_Rating) #removing the "age string"
            Age_Rating = re.sub("\+","", Age_Rating) # removing the plus sign(+) so that it can be stored as numeric to allow correct sorting
            Age_Rating = int(Age_Rating)
            
        except:
            Age_Rating = ""
            
        App_reviews = {"App_Name":App_Name,"Review":Review, "Platforms":Platforms, "Link":Link, "Date_Published":Date_Published, "Age_Rating":Age_Rating}
        dta = dta.append(App_reviews, ignore_index = True)
    
######
    
############
now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time, ": Writing the output...")
############

#Saving the output to CSV
dta.to_csv("app reviews and ratings.csv", sep = ",", na_rep="", index=False) #need to set seperator as ; because there are 

############
now = datetime.now()
print("Current Time =", current_time, ": The full code is run, check the output in the directory...")
############

timeDif = now - before
print("Total time: ",str(timeDif.seconds), " Seconds")
