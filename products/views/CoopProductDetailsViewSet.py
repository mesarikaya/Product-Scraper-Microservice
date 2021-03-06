import json
import logging
from decimal import Decimal

import jsonpickle
import requests

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from products.serializers import CoopProductDetailsSerializer
from products.models import CoopProduct
from products.models import CoopProductDetails
from products.views.helpers import create_batch_product_details_task
from products.views.helpers import apply_regex
from products.views import AbstractProductDetailsViewSet


class CoopProductDetailsViewSet(AbstractProductDetailsViewSet):
    """Enable CRUD operations for AH Products Details Table from retrieved API call JSON resources"""

    def __init__(self):
        super()

    def get(self):
        """Get all details of all products"""
        """TODO: Create a specific view for admin and other users."""
        """TODO: Create a specific product item search."""
        CoopProductDetails.objects.all()

    def post(self, request, format=None):
        batch_size = request.data['batch_size']
        is_allowed = request.data['is_allowed']
        if is_allowed and batch_size >= 0 and batch_size:
            try:
                create_batch_product_details_task(product_class=CoopProduct,
                                                  column_name='product_url',
                                                  view_json=jsonpickle.encode(CoopProductDetailsViewSet),
                                                  serializer_json=jsonpickle.encode(CoopProductDetailsSerializer),
                                                  task_name='get_Coop_product_details',
                                                  batch_size=batch_size, min_time_delay=1, max_time_delay=5)
                print("Coop Task is created")
                return Response("Success", status=status.HTTP_201_CREATED)
            except Exception as e:
                print(Exception(e))
                return Response("Error in execution", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied", status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    def get_json_data(product_url):
        headers = {'User-agent': 'PostmanRuntime/7.24.0'}
        try:
            r = requests.get(url=product_url, headers=headers)
            text = r.content.decode("utf-8")
            result = CoopProductDetailsViewSet.map_product_details(text)
        except Exception as e:
            print("Get json data error:", Exception(e))
        else:
            return result

    @staticmethod
    def map_product_details(text):
        """Map the external api json to a dictionary map that is in line with AH Product Details model"""
        try:
            data = {
                "title": apply_regex(text, 'altHead head1" itemprop="name">(.*?)</h1>', 31, 5)[:100],
                "description": "",
                "price_unit_info": None,
                "price_unit_info_unit_size": "",
                "image_url": apply_regex(text, 'data-srcset="(.*?).jpg', 13, 0).replace("&#47;", "/"),
                "summary": "",
                "hq_id": None,
                "properties": "",
                "is_medicine": None
            }

            product_details = clean_product_details(
                apply_regex(text, 'data-type="details"\ndata-product="(.*?)"', 33, 1))
            product_id = product_details.get('id', -1)
            category = list(CoopProduct.objects.filter(product_id=product_id).values_list('category', flat=True))
            if not category:
                category = ""
            else:
                category = category[0]

            price_now = product_details.get('price', None)
            if price_now is not None:
                price_now = Decimal(price_now)

            data.setdefault('product_id', int(product_id))
            data.setdefault('price_now', price_now)
            data.setdefault('price_now_unit_size', product_details.get('variant', ""))
            data.setdefault('brand', product_details.get('brand', ""))
            data.setdefault('category', category)
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
