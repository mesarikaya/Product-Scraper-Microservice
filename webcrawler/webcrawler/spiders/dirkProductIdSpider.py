import json
import scrapy

from scraper_api import ScraperAPIClient
from ..load_properties import load_properties


class DirkProductIdSpider(scrapy.Spider):
    name = "dirk_products"

    def __init__(self):
        super()
        self.properties = load_properties()

    def start_requests(self):
        secret = self.properties.properties['Scraper_secret']
        print("Properties:", self.properties.properties)
        scrape_url = "Scraper_Dirk_Scrape_url"
        client = ScraperAPIClient(secret)

        for i in self.properties.properties.keys():
            if str(i).startswith(scrape_url):
                url = self.properties.properties[i]
                property_value = self.properties.properties[i].split("/")
                priority = i.split("_")[4]
                category = property_value[4]
                print("Calling yield function for url: ", url)
                yield scrapy.Request(
                    client.scrapyGet(url=url),
                    self.parse, dont_filter=True, priority=int(priority), meta={'category': category})

    def parse(self, response):
        # print("Inside parse function", response.text)
        rows = response.xpath('//a/@href').extract()
        # print("Rows are:", rows)
        with open("dirk_product_ids.json", "a") as file:
            for index, product in enumerate(rows):
                if '/boodschappen/' in product:
                    print("Product:", product)
                    json.dump({
                        'product_id': product,
                        'category': response.meta['category']
                    }, file)
                    if index < len(rows) - 1:
                        file.write(',')
