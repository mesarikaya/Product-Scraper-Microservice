import configparser
import os
from collections import defaultdict

from jproperties import Properties

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_properties():
    config = configparser.ConfigParser()
    properties = defaultdict()
    properties = Properties()
    with open(BASE_DIR + "\\webcrawler\\resources\\application_dev.properties", "rb") as f:
        properties.load(f, "utf-8")

    return properties
