import configparser
import os
from collections import defaultdict

from jproperties import Properties

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_properties():
    config = configparser.ConfigParser()
    properties = defaultdict()
    properties = Properties()
    print("Properties file directory:", BASE_DIR + "\\webcrawler\\application_dev.properties")
    with open(BASE_DIR + "\\webcrawler\\application_dev.properties", "rb") as f:
        properties.load(f, "utf-8")

    print([i for i in properties.properties.keys() if str(i).startswith("Scraper_AH_scrape_url")])
    return properties


load_properties()
