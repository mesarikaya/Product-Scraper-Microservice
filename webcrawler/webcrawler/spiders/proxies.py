import requests
import traceback
import json
import scrapy
import sys

from scrapy.spiders import CrawlSpider
from itertools import cycle
from lxml.html import fromstring
from scraper_api import ScraperAPIClient

class ProxyList(CrawlSpider):

    @classmethod
    def get_proxies_from_scraper_api(cls, proxy_count=10):
        client = ScraperAPIClient('3af7d62e85b75e0271d32f245107a240')
        proxies = set()

        for i in range(1,proxy_count):
            result = client.get(url = 'http://httpbin.org/ip').text
            json_data = json.loads(result)
            print(json_data);
            proxies.add(json_data["origin"])

        print(proxies)

        return proxies

        
        
        # Scrapy users can simply replace the urls in their start_urls and parse function
        # Note for Scrapy, you should not use DOWNLOAD_DELAY and
        # RANDOMIZE_DOWNLOAD_DELAY, these will lower your concurrency and are not
        # needed with our API

    # ...other scrapy setup code
    # start_urls =[client.scrapyGet(url = 'http://httpbin.org/ip')]
    #def parse(self, response):

    # ...your parsing logic here
    # yield scrapy.Request(client.scrapyGet(url = 'http://httpbin.org/ip'), self.parse)

    @classmethod
    def get_proxies(cls, search_size=50):
        url = 'https://free-proxy-list.net/'
        response = requests.get(url)
        parser = fromstring(response.text)
        proxies = set()
        for i in parser.xpath('//tbody/tr')[:search_size]:
            if i.xpath('.//td[7][contains(text(),"yes")]'):
                # Grabbing IP and corresponding PORT
                proxy = ":".join([i.xpath('.//td[1]/text()')[0], i.xpath('.//td[2]/text()')[0]])
                proxies.add(proxy)
        return proxies

    @classmethod
    def rotate_proxies(cls, proxyList=set()):

        proxy_pool = cycle(proxyList)
        print("Provided proxy list: ", proxyList)
        url = 'https://httpbin.org/ip'
        for i in range(1, len(proxyList)):
            #Get a proxy from the pool
            proxy = next(proxy_pool)

            print("Request #%d"%i)
            try:
                response = requests.get(url,proxies={"http": proxy, "https": proxy})
                json_data = response.json()
                #item = ProxyItem()
                #item["proxy"] = json_data["origin"]
                print("Successful proxy:", item["proxy"])
                #return item
            except:
                #Most free proxies will often get connection errors. You will have retry the entire request using another proxy to work. 
                #We will just skip retries and we are only downloading a single url 
                print("Skipping. Connnection error")
                print("Unexpected error:", sys.exc_info()[0])
                #raise

        #