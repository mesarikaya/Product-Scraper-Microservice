import json
import scrapy

from scraper_api import ScraperAPIClient
from ..load_properties import load_properties


class DeenProductIdSpider(scrapy.Spider):
    name = "deen_products"

    def __init__(self):
        super()
        self.properties = load_properties()

    def start_requests(self):
        secret = self.properties.properties['Scraper_secret']
        scrape_url = "Scraper_Deen_scrape_url_1"
        client = ScraperAPIClient(secret)
        url = self.properties.properties[scrape_url] + '?items=6000'
        print("URl is:", url)
        yield scrapy.Request(client.scrapyGet(url=url), self.parse, dont_filter=True)

    def parse(self, response):
        rows = response.xpath('//a/@href').extract()
        with open("deen_product_ids.json", "a") as file:
            for index, product in enumerate(rows):
                if '/product/' in product:
                    print("Product:", product)
                    json.dump({'product_id': product}, file)
                    if index < len(rows) - 1:
                        file.write(',')
