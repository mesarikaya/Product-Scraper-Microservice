import logging
import random

import jsonpickle
import requests

from datetime import timedelta
from background_task import background
from django.utils import timezone
from collections import defaultdict
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from products.views.helpers import create_batch_product_details_task
from products.views.AbstractProductDetailsViewSet import AbstractProductDetailsViewSet
from products.models import AlbertHeijnProductDetails, AlbertHeijnProduct
from products.serializers import AlbertHeijnProductDetailsSerializer


class AHProductDetailsViewSet(AbstractProductDetailsViewSet):
    """Enable CRUD operations for AH Products Details Table from retrieved API call JSON resources"""

    def __init__(self):
        super()

    def get(self):
        """Get all details of all products"""
        """TODO: Create a specific view for admin and other users."""
        """TODO: Create a specific product item search."""
        AlbertHeijnProductDetails.objects.all()

    def post(self, request, format=None):
        batch_size = request.data['batch_size']
        is_allowed = request.data['is_allowed']
        if is_allowed and batch_size >= 0 and batch_size:
            try:
                create_batch_product_details_task(product_class=AlbertHeijnProduct,
                                                  column_name='product_id',
                                                  view_json=jsonpickle.encode(AHProductDetailsViewSet),
                                                  serializer_json=jsonpickle.encode(AlbertHeijnProductDetailsSerializer),
                                                  task_name='get_AH_product_details',
                                                  batch_size=10, min_time_delay=1, max_time_delay=5)
                return Response("Success", status=status.HTTP_201_CREATED)
            except Exception as e:
                logging.debug("Unexpected exception:", Exception(e))
                return Response("Error in execution", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied", status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_json_data(product_id):
        """TODO: Create an env variable for this url"""
        URL = "https://www.ah.nl/zoeken/api/products/product"
        try:
            product_id = product_id
            PARAMS = {'webshopId': product_id}
            r = requests.get(url=URL, params=PARAMS)
            data = r.json()
            result = AHProductDetailsViewSet.map_product_details(data)
        except Exception as e:
            logging.debug("Json serialization exception:", Exception(e))
        else:
            return result

    @staticmethod
    def map_product_details(json_value):
        """Map the external api json to a dictionary map that is in line with AH Product Details model"""

        data = defaultdict()
        try:
            data.setdefault('title', json_value.get('card', {}).get('products', [])[0].get('title', ""))
            data.setdefault('product_id', json_value.get('card', {}).get('products', [])[0].get('id', -1))
            data.setdefault('summary', json_value.get('card', {}).get('products', [])[0].get('summary', ""))
            data.setdefault('is_available', json_value.get('card', {}).get('products', [])[0].get('orderable', None))
            products = json_value.get('card', {}).get('products', [])
            if not products:
                data.setdefault('price_now', None)
                data.setdefault('price_now_unit_size', "")
            else:
                data.setdefault('price_now', products[0].get('price', {}).get('now'))
                data.setdefault('price_now_unit_size', products[0].get('price', {}).get('unitSize'))
            image = json_value.get('card', {}).get('products', [])[0].get('images', {})
            if not image:
                data.setdefault('image_url', "")
            else:
                data.setdefault('image_url', image[0].get('url', ""))
            data.setdefault('brand', json_value.get('card', {}).get('products', [])[0].get('brand', ""))
            data.setdefault('category', json_value.get('card', {}).get('products', [])[0].get('category', ""))
            data.setdefault('hq_id', json_value.get('card', {}).get('products', [])[0].get('hqId', None))
            data.setdefault('is_medicine', json_value.get('card', {}).get('meta', {}).get('isMedicine', None))
            data.setdefault('properties', '-'.join(json_value.get('card', {}).get('products', [])[0]
                            .get('properties', {}).get('lifestyle', [])))
            description = json_value.get('card', {}).get('meta', {}).get('descriptions', [])
            if not description:
                data.setdefault('description', "")
            else:
                data.setdefault('description', description[0])
            data.setdefault('catalog_id', json_value.get('card', {}).get('products', [])[0].get('itemCatalogId', None))
            data.setdefault('price_unit_info', json_value.get('card', {}).get('products', [])[0].get('price', {})
                            .get('unitInfo', {}).get('price', None))
            data.setdefault('price_unit_info_unit_size',
                            json_value.get('card', {}).get('products', [])[0].get('price', {})
                            .get('unitInfo', {}).get('description', ""))
        except KeyError as e:
            logging.debug("Key Error:", e, json_value)
        except IndexError as e:
            logging.debug("Index Error: ", e)
        except Exception as e:
            logging.debug("Exception: ", e, json_value)
        else:
            return data
