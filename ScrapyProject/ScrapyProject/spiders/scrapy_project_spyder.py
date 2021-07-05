
#####Written by: Joao Claudio Macosso

#####
# In this code we scrape app reviews, ratings and release date of popular apps on multiple devices
# the data is being scraped from https://www.commonsensemedia.org 
#Warning: these are not official reviews on respective platforms. unlike playstore and app store where 
#the user can only review apps that thety have used, this website does not have such restriction, 
#thus leading to questions regarding the quality of reviews. However, these reviews are usually made by professionals, hence reducing risks of spurious reviews
#This scraper is written using Scrapy framework
#Scrapy must be installed in order to run the code successully
#in the comand line change directory to the project directory
# scrapy crawl 

limit_page = False ## set to false to read all pages, else keep True to readonly first 100 pages



from datetime import datetime, timedelta
before = datetime.now()
current_time_1 = before.strftime("%H:%M:%S")
print("Current Time =", current_time_1)

from datetime import datetime, timedelta
before = datetime.now()
current_time_1 = before.strftime("%H:%M:%S")
print("Current Time =", current_time_1)




import scrapy
from scrapy.crawler import CrawlerProcess
import re


if limit_page == True:
    max_pages = 101
else:
    max_pages = 254

home = 'https://www.commonsensemedia.org'
class ScrapyProjectSpider(scrapy.Spider):
    name = 'scrapy_project_spyder'
    allowed_domains = ['https://www.commonsensemedia.org/']
    
    start_urls=["https://www.commonsensemedia.org/app-reviews"] #starting a link with the first page in which I will append the next pages
    for i in range(1,max_pages): #set the number of pages that will be scraped, the maximum number is 243 pages
        start_urls.append("https://www.commonsensemedia.org/app-reviews"+ "?page="+str(i))
    

    def parse(self, response):
        responses = response.css('div.view-content > div')
        for i in responses:
            try:
                link = home + i.css('.field-content a::attr(href)').extract()[0]
            except:
                link = ""
                
            try:
                name = i.css('.field-content a::text').get()
                name = re.sub(',','',name) #remove commas in the name
            except:
                name = ""
                
            try:
                age =  i.css('.csm-green-age:first-child::text').get()
                age = re.sub('age ','',age)
                age = re.sub("\+","", age)
            except:
                age = ""
                
            try:
                star = i.css('.csm-review:first-child::attr(class)').get()[26]
            except:
                star = ""
            
            try:
                devices = i.css('em.field-content::text').get()
            except:
                devices
            try:
                publish_date = i.css('.date-display-single::attr(content)').get()[0:10]
            except:
                publish_date
                
            
            yield {'App_Name' : name,
                   'Review' : star,
                   'Platforms' : devices,
                   'Link' : link,
                   'Age_Rating' : age,
                   "Date_Published":publish_date
                }
   

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time, ": Writing the output...")
############
now = datetime.now()
print("Current Time =", current_time, ": The full code is run, check the output in the directory...")
############

timeDif = now - before
print("Total time: ",str(timeDif.seconds), " Seconds")


# process = CrawlerProcess()
# process.crawl(ScrapyProjectSpider)
# process.start()

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("Current Time =", current_time, ": Writing the output...")
############

now = datetime.now()
print("Current Time =", current_time, ": The full code is run, check the output in the directory...")
############

timeDif = now - before
print("Total time: ",str(timeDif.seconds), " Seconds")

############
