import requests
import traceback
import json
import scrapy
import sys

from scrapy.spiders import CrawlSpider
from itertools import cycle
from lxml.html import fromstring

class ProxyList(CrawlSpider):

    @classmethod
    def get_proxies(cls, search_size=50):
        url = 'https://free-proxy-list.net/'
        response = requests.get(url)
        parser = fromstring(response.text)
        proxies = set()
        for i in parser.xpath('//tbody/tr')[:search_size]:
            print("i value is: ", i.xpath('.//td[1]/text()'),"-", i.xpath('.//td[2]/text()'),"-", i.xpath('.//td[3]/text()'),"-", i.xpath('.//td[4]/text()'), ,"-", i.xpath('.//td[5]/text()'),,"-", i.xpath('.//td[6]/text()'),,"-", i.xpath('.//td[7]/text()'))
            if i.xpath('.//td[3][contains(text(),"HTTPS")]') and i.xpath('.//td[4][contains(text(),"High Anonymous")]'):
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