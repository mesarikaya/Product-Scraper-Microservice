import json
import scrapy

from scrapy import Selector
from selenium import webdriver
from ..load_properties import load_properties


def get_start_urls():
    properties = load_properties()
    scrape_url = properties.properties["Scraper_Jumbo_scrape_url_1"]
    urls = list()
    for page in range(0, 750):
        url = scrape_url + str(page) + '&pageSize=25'
        urls.append(url)

    return urls


class JumboProductIdSpider(scrapy.Spider):
    name = "jumbo_products"
    start_urls = get_start_urls()
    print("start_urls: ", start_urls[0:5])

    def __init__(self):
        super()

    def parse(self, response):
        driver = webdriver.Chrome()
        driver.implicitly_wait(20)
        driver.set_page_load_timeout(20)
        driver.set_script_timeout(20)
        driver.minimize_window()
        driver.get(response.url)
        scrapy_selector = Selector(text=driver.page_source)
        rows = scrapy_selector.xpath("//a[contains(@class,'jum-product-card__image')]/@href").extract()
        with open("jumbo_product_ids.json.json", "a") as file:
            for index, product in enumerate(rows):
                print("row: ", product)
                json.dump({
                    'product_id': product
                }, file)
                if index < len(rows) - 1:
                    file.write(',')
        driver.close()
