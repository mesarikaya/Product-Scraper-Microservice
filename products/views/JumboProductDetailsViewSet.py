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
from products.models import JumboProductDetails
from products.serializers import JumboProductDetailsSerializer
from products.models import JumboProduct
from products.views.helpers import create_batch_product_details_task
from products.views.helpers import apply_regex
from products.views import AbstractProductDetailsViewSet


class JumboProductDetailsViewSet(AbstractProductDetailsViewSet):
    """Enable CRUD operations for Jumbo Products Details Table from retrieved API call JSON resources"""

    def __init__(self):
        super()

    def get(self):
        """Get all details of all products"""
        """TODO: Create a specific view for admin and other users."""
        """TODO: Create a specific product item search."""
        JumboProductDetails.objects.all()

    def post(self, request, format=None):
        """TODO: Create an env variable for this url"""
        batch_size = request.data['batch_size']
        is_allowed = request.data['is_allowed']
        if is_allowed and batch_size >= 0 and batch_size:
            try:
                create_batch_product_details_task(product_class=JumboProduct,
                                                  column_name='product_id',
                                                  view_json=jsonpickle.encode(JumboProductDetailsViewSet),
                                                  serializer_json=jsonpickle.encode(JumboProductDetailsSerializer),
                                                  task_name='get_Jumbo_product_details',
                                                  batch_size=10, min_time_delay=3, max_time_delay=7)
                return Response("Success", status=status.HTTP_201_CREATED)
            except Exception as e:
                logging.debug("Unexpected Exception: ", Exception(e))
                return Response("Error in execution", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied", status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_json_data(product_id):
        """TODO: Create an env variable for this url"""
        base_url = 'https://www.jumbo.com'
        headers = {'User-agent': 'PostmanRuntime/7.24.0'}
        try:
            r = requests.get(url=base_url + product_id, headers=headers)
            text = r.content.decode("utf-8")
            result = JumboProductDetailsViewSet.map_product_details(text)
        except Exception as e:
            logging.info("Get json data error:", Exception(e))
        else:
            return result

    @staticmethod
    def map_product_details(text):
        text = ' '.join(text.split())
        try:
            try:
                general_price_info = apply_regex(text, 'jum-comparative-price">((.*?))</span>', 24, 8).replace("&#47;",
                                                                                                               ";")
                price_unit_info = Decimal(general_price_info.split(";")[0].replace(',', '.'))
                price_unit_info_unit_size = general_price_info.split(";")[1]
            except Exception as e:
                price_unit_info = None
                price_unit_info_unit_size = ""

            data = {
                "description": apply_regex(text, '<h3>Productomschrijving</h3>(.*?)</div>', 28, 6)[:100],
                "price_now_unit_size": apply_regex(text, 'jum-pack-size">(.*?)</span>', 15, 7),
                "price_unit_info": price_unit_info,
                "price_unit_info_unit_size": price_unit_info_unit_size,
                "image_url": apply_regex(text, 'resources-jum-hr-src="(.*?)"', 17, 1).replace("&#47;", "/"),
                "summary": apply_regex(text, '<div class="jum-summary-description"> <p>(.*?)</p>', 41, 4),
                "hq_id": None,
                "properties": "",
                "is_medicine": None
            }
            product_details = clean_product_details(apply_regex(text, 'data-jum-product-details="(.*?)"', 26, 1))
            data.setdefault('title', product_details.get('name', ""))
            data.setdefault('price_now', product_details.get('price', None))
            data.setdefault('brand', product_details.get('brand', ""))
            data.setdefault('category', product_details.get('category', ""))
            data.setdefault('product_id', product_details.get('id', "-1"))
        except KeyError as e:
            logging.debug("Key Error:", e, text)
        except IndexError as e:
            logging.debug("Index Error: ", e)
        except Exception as e:
            logging.debug("Exception: ", e, text)
        else:
            return data


def clean_product_details(text):
    try:
        result = json.loads(text
                            .replace("&quot;", "\"")
                            .replace("\\", "")
                            .replace("&#47;", "-"))
    except Exception as e:
        logging.info("Exception during json load:", e)
        return {'name': '', 'id': '-1', 'price': None, 'brand': '', 'category': ''}
    else:
        return result
