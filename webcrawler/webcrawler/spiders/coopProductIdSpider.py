import json
import scrapy

from scraper_api import ScraperAPIClient
from ..load_properties import load_properties


class CoopProductIdSpider(scrapy.Spider):
    name = "coop_products"

    def __init__(self):
        super()
        self.properties = load_properties()

    def start_requests(self):
        secret = self.properties.properties['Scraper_secret']
        print("Properties:", self.properties.properties)
        scrape_url = "Scraper_Coop_scrape_url"
        client = ScraperAPIClient(secret)

        start_urls = list()
        priorities = list()
        categories = list()
        for i in self.properties.properties.keys():
            if str(i).startswith(scrape_url):
                property_value = self.properties.properties[i].split(";")
                start_urls.append(property_value[0])
                priorities.append(i.split("_")[4])
                categories.append(property_value[1])
        print("Key start urls are:", start_urls, "Priorities:", priorities)

        for priority, url, category in zip(priorities, start_urls, categories):
            print("Calling yield function for url: ", url)
            yield scrapy.Request(
                client.scrapyGet(url=url),
                self.parse, dont_filter=True, priority=int(priority), meta={'category': category})

    def parse(self, response):
        # print("Inside parse function", response.text)
        rows = response.xpath('//a/@href').extract()
        # print("Rows are:", rows)
        with open("coop_product_ids.json", "a") as file:
            for index, product in enumerate(rows):
                if '/product/' in product:
                    print("Product:", product)
                    json.dump({
                        'product_id': product,
                        'category': response.meta['category']
                    }, file)
                    if index < len(rows) - 1:
                        file.write(',')
