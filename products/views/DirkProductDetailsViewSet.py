import json
import logging
from decimal import Decimal
import jsonpickle
import requests
from rest_framework import status
from rest_framework.response import Response
from products.serializers import DirkProductDetailsSerializer
from products.models import DirkProduct
from products.models import DirkProductDetails
from products.views.helpers import create_batch_product_details_task
from products.views.helpers import apply_regex
from products.views import AbstractProductDetailsViewSet
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import chromedriver_binary  # Adds chromedriver binary to path


class DirkProductDetailsViewSet(AbstractProductDetailsViewSet):
    """Enable CRUD operations for Dirk Products Details Table from retrieved API call JSON resources"""

    def __init__(self):
        super()

    def get(self):
        """Get all details of all products"""
        """TODO: Create a specific view for admin and other users."""
        """TODO: Create a specific product item search."""
        DirkProductDetails.objects.all()

    def post(self, request, format=None):

        batch_size = request.data['batch_size']
        is_allowed = request.data['is_allowed']
        if is_allowed and batch_size >= 0 and batch_size:
            try:
                create_batch_product_details_task(product_class=DirkProduct,
                                                  column_name='product_url',
                                                  view_json=jsonpickle.encode(DirkProductDetailsViewSet),
                                                  serializer_json=jsonpickle.encode(DirkProductDetailsSerializer),
                                                  task_name='get_Dirk_product_details',
                                                  batch_size=batch_size, min_time_delay=3, max_time_delay=7)
                print("Dirk Task is created")
                return Response("Success", status=status.HTTP_201_CREATED)
            except Exception as e:
                print(Exception(e))
                return Response("Error in execution", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied", status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_json_data(product_url):
        # Create headless chrome driver

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("window-size=1400,2100")
        chrome_options.add_argument('--disable-gpu')
        # driver = webdriver.Chrome(chrome_options=chrome_options)
        # driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',chrome_options=chrome_options)
        driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
        driver.implicitly_wait(5)
        driver.set_page_load_timeout(5)
        driver.set_script_timeout(5)
        # headers = {'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0'}

        try:
            driver.get(product_url)
            page_source = driver.page_source
            # print("Page source is:", page_source)
            # scrapy_selector = Selector(text=driver.page_source)
            # rows = scrapy_selector.xpath("//a[contains(@class,'jum-product-card__image')]/@href").extract()
            """r = requests.get(url=product_url, headers=headers)
            text = page_source.content.decode("utf-8")"""
            result = DirkProductDetailsViewSet.map_product_details(page_source, product_url)
        except Exception as e:
            driver.close()
            print("Get json data error:", Exception(e))
        else:
            driver.close()
            return result

    @staticmethod
    def map_product_details(text, product_url):
        """Map the external api json to a dictionary map that is in line with AH Product Details model"""
        try:
            price_part_1 = apply_regex(text, '"product-card__price__euros">(.*?)</span>', 29, 7).replace(".", "")
            print("Price part 1:", price_part_1)
            price_part_2 = apply_regex(text, '"product-card__price__cents">(.*?)</span>', 29, 7).replace("", "")
            print("Price part 2:", price_part_2)

            price = Decimal(price_part_1 + "." + price_part_2)

            url_split = product_url.split("/")
            if len(url_split) > 3:
                product_id = url_split[-1]
                category = url_split[3]
            else:
                product_id = -1
                category = ""

            image_url = apply_regex(text, '"product-details__image(.*?).png',
                                         23, 0).replace("&#47;", "/")\
                .replace(" ", "").replace(">", "").replace("<", "")

            image_url = apply_regex(image_url, 'src="(.*?).png',
                                         5, 0)
            data = {
                "title": apply_regex(text, '<title>(.*?)</title>', 7, 8)[:100],
                "product_id": int(product_id),
                "description": apply_regex(text, 'Omschrijving</h3>(.*?)</div>', 82, 6),
                "price_now": price,
                "price_now_unit_size": apply_regex(text, 'product-details__info__subtitle">(.*?)</span>',
                                                   33, 7).strip(),
                "price_unit_info": None,
                "price_unit_info_unit_size": "",
                "image_url": image_url,
                "summary": "",
                "catalog_id": None,
                "brand": "",
                "category": category,
                "is_available": True,
                "hq_id": None,
                "properties": "",
                "is_medicine": None
            }
        except KeyError as e:
            print("Key Error:", e)
        except IndexError as e:
            print("Index Error: ", e)
        except Exception as e:
            print("Exception: ", e)
        else:
            return data


def clean_product_details(text):
    try:
        result = json.loads(text
                            .replace("&quot;", "\"")
                            .replace("\\", "")
                            .replace("&#47;", "-")
                            .replace("\"{", "{")
                            .replace("}\"", "}"))
    except Exception as e:
        print("Exception during json load:", e)
        return {'id': -1, 'price': None, 'variant': ''}
    else:
        return result
