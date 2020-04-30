import logging
import random

import jsonpickle
import requests
import re
import json

from background_task import background
from decimal import Decimal
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import DeenProductDetails
from products.serializers import DeenProductDetailsSerializer
from products.models import DeenProduct
from products.views.helpers import create_batch_product_details_task
from products.views.helpers import apply_regex
from products.views import AbstractProductDetailsViewSet


class DeenProductDetailsViewSet(AbstractProductDetailsViewSet):
    """Enable CRUD operations for Deen Products Details Table from retrieved API call JSON resources"""

    def __init__(self):
        super()

    def get(self):
        """Get all details of all products"""
        """TODO: Create a specific view for admin and other users."""
        """TODO: Create a specific product item search."""
        DeenProductDetails.objects.all()

    def post(self, request, format=None):
        """TODO: Create an env variable for this url"""
        batch_size = request.data['batch_size']
        is_allowed = request.data['is_allowed']
        if is_allowed and batch_size >= 0 and batch_size:
            try:
                create_batch_product_details_task(product_class=DeenProduct,
                                                  column_name='product_id',
                                                  view_json=jsonpickle.encode(DeenProductDetailsViewSet),
                                                  serializer_json=jsonpickle.encode(DeenProductDetailsSerializer),
                                                  task_name='get_Deen_product_details',
                                                  batch_size=10, min_time_delay=1, max_time_delay=5)
                return Response("Success", status=status.HTTP_201_CREATED)
            except Exception as e:
                print("Unexpected Exception: ", Exception(e))
                return Response("Error in execution", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied", status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_json_data(product_id):
        """TODO: Create an env variable for this url"""
        base_url = 'https://www.deen.nl/'
        headers = {'User-agent': 'PostmanRuntime/7.24.0'}
        print("Searching product id:", product_id)
        try:
            r = requests.get(url=base_url + product_id, headers=headers)
            text = r.content.decode("utf-8")
            result = DeenProductDetailsViewSet.map_product_details(text)
        except Exception as e:
            raise Exception(e)
        else:
            return result

    @staticmethod
    def map_product_details(text):
        text = ' '.join(text.split())
        try:
            category = apply_regex(text, 'href="/boodschappen/(.*?)"', 20, 1).split("/")[-1][:200]
        except Exception as e:
            category = ""

        try:
            data = {
                "title": apply_regex(text, '<h1 itemprop="name">(.*?)</h1>', 20, 5).replace("&#39;", "é")[:200],
                "product_id": apply_regex(text, '<meta itemprop="sku" content="(.*?)"', 30, 1),
                "description": apply_regex(text, 'description">(.*?)<', 14, 2),
                "price_now": apply_regex(text, 'price: (.*?),', 8, 2).replace(",", "."),
                "price_now_unit_size": apply_regex(text, 'Gewicht</h3>(.*?)<', 12, 1).strip(),
                "price_unit_info": None,
                "price_unit_info_unit_size": "",
                "image_url": apply_regex(text, 'photo: (.*?),', 8, 2).replace("&#47;", "/"),
                "summary": "",
                "catalog_id": None,
                "brand": apply_regex(text, 'itemprop="brand" content="(.*?)"', 26, 1).replace("&#39;","'").replace("&#39;", "é"),
                "category": category,
                "is_available": True,
                "hq_id": None,
                "properties": "",
                "is_medicine": None
            }
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
        result = json.loads(text
                            .replace("&quot;", "\"")
                            .replace("\\", "")
                            .replace("&#47;", "-"))
    except Exception as e:
        print("Exception during json load:", e)
        return {'name': '', 'id': '-1', 'price': None, 'brand': '', 'category': ''}
    else:
        return result
