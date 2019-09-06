# -*- coding: utf-8 -*-
import scrapy
import csv
import os
from scrapy.crawler import CrawlerProcess
import time
import lxml
from lxml import html
import openpyxl
import re




class AlibabaCrawlerSpider(scrapy.Spider):
    name = 'alibaba_crawler'
    allowed_domains = ['']
    start_urls = ['']


    f = open('youtube.csv', 'w')
    f.write('url,name,subscribers,views,email,email_get_from,Twitter,Facebook,Instagram,search_keyword')


    def start_requests(self):
        """Read keywords from keywords file amd construct the search URL"""

        # with open(os.path.join(os.path.dirname(__file__), "keywords.csv")) as search_keywords:
        #     for keyword in csv.DictReader(search_keywords):
        #         search_text=keyword["keyword"]
        searchs = ["streetwear","street style","men's fashion","clothing unboxing",
                   "menswear","sweatpants","fashion stylist","sneaker unboxing",
                   "sneaker reviews","fit pics","loungewear","sneakerheads","mnml clothing",
                   "mnml.la","john elliott shirt","john elliott hoodie","mackweldon.com","off-white review","yeezy reviews"]
        #searchs = ['streetwear']

        for search_text in searchs:

            #search_text='Toothbrushes'
            url="https://search.yahoo.com/search?p=site:youtube.com/channel%20%22"+str(search_text)+"%22"
            # The meta is used to send our search text into the parser as metadata
            yield scrapy.Request(url, callback = self.parse, meta = {"search_text": search_text,"page":2},dont_filter=True)


    def parse(self, response):
        search_keyword=response.meta["search_text"]

        All_link = response.xpath('//*[@class="title"]/a[contains(@href,"youtube.com/")]/@href').extract()
        youtube_links = []
        for title in All_link:
            main_url = ''
            if '/channel/' in title:
                url = title.split('youtube.com/channel/', 1)[1]
                if '/' in url:
                    url = url.split('/', 1)[0]
                main_url = 'https://www.youtube.com/channel/' + url + '/about'
            if '/user/' in title:
                url = title.split('youtube.com/user/', 1)[1]
                if '/' in url:
                    url = url.split('/', 1)[0]

                main_url = 'https://www.youtube.com/user/' + url + '/about'
            if main_url != '':
                youtube_links.append(main_url)
                
        for link in youtube_links:
            yield scrapy.Request(link, callback = self.get_data, meta = {"search_text": search_keyword,"page":2},dont_filter=True)

        next_page = response.xpath('//*[@class="next"]/@href').extract_first()
        if next_page != None:
            yield scrapy.Request(next_page, callback = self.parse, meta = {"search_text": search_keyword,"page":2},dont_filter=True)
    def get_data(self, response):
        #print(response)
        strhtml = response.body
        strhtml = strhtml.decode('utf-8')
        f = open('youtube.html','w')
        f.write(strhtml)
        f.close()

        search_keyword=response.meta["search_text"]

        try:
            subscribers = response.xpath("//span[contains(text(),' subscribers')]/b/text()").extract_first()
            if subscribers != None:
                subscribers = str(subscribers).replace('subscribers', '').replace(',', '').strip()
            if subscribers == None or subscribers == []:
                subscribers = response.xpath("//span[contains(text(),' subscriber')]/b/text()").extract_first()
                if subscribers != None:
                    subscribers = str(subscribers).replace('subscriber', '').replace(',', '').strip()
            if subscribers == None:
                subscribers = ''
            views = response.xpath("//*[contains(text(),' •')]/b/text()").extract_first()
            if views != None:
                views = str(views).replace('views', '').replace(',', '').strip()
            if views == None or views == []:
                views = response.xpath("//*[contains(text(),' views')]/b/text()").extract_first()
                if views != None:
                    views = str(views).replace('views', '').replace(',', '').strip()
            if views == None:
                views = ''

            name = response.xpath('//*[@class="qualified-channel-title-text"]/a/text()').extract_first()
            if name != None:
                name = str(name).replace(',', '').strip()
            if name == None:
                name = ''

            Twitter = response.xpath('//*[@title="Twitter"]/@href').extract_first()
            if Twitter != None:
                Twitter = str(Twitter).replace(',', '').strip()
            if Twitter == None:
                Twitter = ''

            Facebook = response.xpath('//*[@title="Facebook"]/@href').extract_first()
            if Facebook != None:
                Facebook = str(Facebook).replace(',', '').strip()
            if Facebook == None:
                Facebook = ''

            Instagram = response.xpath('//*[@title="Instagram"]/@href').extract_first()
            if Instagram != None:
                Instagram = str(Instagram).replace(',', '').strip()
            if Instagram == None:
                Instagram = ''

            try:
                email = re.search(r'[\w\.-]+@[\w\.-]+', strhtml)
                email = email.group(0)
                descript = 'page'
            except:
                email = ''
                descript = ''
            print(response.url)
        except Exception as e:
            name = ''
            subscribers = ''
            views = ''
            email = ''
            descript = ''
            Instagram = ''
            Facebook = ''
            Twitter = ''

        if name != '':
            self.f.write('\n')
            self.f.write(str(response.url).replace('about', '') + ',' + str(name) + ',' + str(subscribers) + ',' + str(
                views) + ',' + str(email) + ',' + str(descript)+ ',' + str(Twitter)+ ',' + str(Facebook)+ ',' + str(Instagram)+ ',' + str(search_keyword))
        
        
    def close(spider, reason):
        spider.f.close()


process = CrawlerProcess({'LOG_ENABLED': False,
                          'CONCURRENT_REQUESTS': 200})
process.crawl(AlibabaCrawlerSpider)
try:
    process.start()
except:
    pass