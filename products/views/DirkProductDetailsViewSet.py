import json
import logging
import jsonpickle
import requests

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from products.serializers import DirkProductDetailsSerializer
from products.models import DirkProduct
from products.models import DirkProductDetails
from products.views.helpers import create_batch_product_details_task
from products.views.helpers import apply_regex
from products.views import AbstractProductDetailsViewSet


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
                                                  batch_size=10, min_time_delay=3, max_time_delay=7)
                return Response("Success", status=status.HTTP_201_CREATED)
            except Exception as e:
                logging.debug(Exception(e))
                return Response("Error in execution", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied", status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_json_data(product_url):
        headers = {'User-agent': 'PostmanRuntime/7.24.0'}
        try:
            r = requests.get(url=product_url, headers=headers)
            text = r.content.decode("utf-8")
            result = DirkProductDetailsViewSet.map_product_details(text, product_url)
        except Exception as e:
            print("Get json data error:", Exception(e))
        else:
            return result

    @staticmethod
    def map_product_details(text, product_url):
        """Map the external api json to a dictionary map that is in line with AH Product Details model"""
        try:
            price_part_1 = apply_regex(text, '"product-card__price__euros"(.*?)</span>', 45, 7).replace(".", "")
            price_part_2 = apply_regex(text, '"product-card__price__cents"(.*?)</span>', 45, 7).replace("", "")
            price = price_part_1 + "." + price_part_2
            print("PRice: ", price)
            url_split = product_url.split("/")
            print("Url split:", url_split)
            if len(url_split) > 3:
                product_id = url_split[-1]
                category = url_split[3]
            else:
                product_id = -1
                category = ""

            data = {
                "title": apply_regex(text, '<title>(.*?)</title>', 7, 8)[:100],
                "product_id": product_id,
                "description": apply_regex(text, 'Omschrijving</h3>(.*?)</div>', 79, 6),
                "price_now": price,
                "price_now_unit_size": apply_regex(text, 'product-details__info__subtitle" (.*?)</span>', 49,
                                                   7).strip(),
                "price_unit_info": None,
                "price_unit_info_unit_size": "",
                "image_url": apply_regex(text, '"product-details__image" (.*?)?width', 59, 6).replace("&#47;", "/"),
                "summary": "",
                "catalog_id": None,
                "brand": "",
                "category": category,
                "is_available": True,
                "hq_id": None,
                "properties": "",
                "is_medicine": None
            }
            # print("Data is: ", resources)
        except KeyError as e:
            logging.debug("Key Error:", e, text)
            raise KeyError(e)
        except IndexError as e:
            logging.debug("Index Error: ", e)
            print("Index error: ", text)
            raise IndexError(e, text)
        except Exception as e:
            logging.debug("Exception: ", e, text)
            raise Exception(e)
        else:
            return data


def clean_product_details(text):
    try:
        print('CLEANED REGEX:', text
              .replace("&quot;", "\"")
              .replace("\\", "")
              .replace("&#47;", "-")
              .replace("\"{", "{")
              .replace("}\"", "}"))
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
