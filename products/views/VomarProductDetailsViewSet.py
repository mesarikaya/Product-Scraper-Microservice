import json
import logging
from decimal import Decimal

import jsonpickle
import requests

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from products.serializers import VomarProductDetailsSerializer
from products.models import VomarProduct
from products.models import VomarProductDetails
from products.views.helpers import create_batch_product_details_task
from products.views.helpers import apply_regex
from products.views import AbstractProductDetailsViewSet


class VomarProductDetailsViewSet(AbstractProductDetailsViewSet):
    """Enable CRUD operations for Vomar Products Details Table from retrieved API call JSON resources"""

    def __init__(self):
        super()

    def get(self):
        """Get all details of all products"""
        """TODO: Create a specific view for admin and other users."""
        """TODO: Create a specific product item search."""
        VomarProductDetails.objects.all()

    def post(self, request, format=None):
        batch_size = request.data['batch_size']
        is_allowed = request.data['is_allowed']

        if is_allowed and batch_size >= 0 and batch_size:
            try:
                create_batch_product_details_task(product_class=VomarProduct,
                                                  column_name='product_id',
                                                  view_json=jsonpickle.encode(VomarProductDetailsViewSet),
                                                  serializer_json=jsonpickle.encode(VomarProductDetailsSerializer),
                                                  task_name='get_Vomar_product_details',
                                                  batch_size=batch_size, min_time_delay=1, max_time_delay=5)
                print("Vomar Task is created")
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
            result = VomarProductDetailsViewSet.map_product_details(text, product_url)
            logging.info("Saving data:", result)
        except Exception as e:
            print("Get json data error:", Exception(e))
        else:
            return result

    @staticmethod
    def map_product_details(text, product_url):
        """Map the external api json to a dictionary map that is in line with Vomar Product Details model"""
        text = ' '.join(text.split())
        try:
            price_part_1 = apply_regex(text, 'class="main">(.*?)</span>', 13, 7).replace(".", "")
            price_part_2 = apply_regex(text, 'class="cents">(.*?)</span>', 14, 7).replace("", "")
            price = price_part_1 + "." + price_part_2

            url_split = product_url.split("/")
            try:
                product_id = product_url
                title = url_split[-1]
                category = list(VomarProduct.objects.filter(product_id=product_url).values_list('category', flat=True))[0]
            except Exception as e:
                product_id = "-1"
                category = ""
                title = ""

            data = {
                "title": title,
                "product_id": product_id,
                "description": apply_regex(text, '<h5>Beschrijving</h5> <p>(.*?)</p>', 25, 4),
                "price_now": Decimal(price),
                "price_now_unit_size": apply_regex(text, 'class="unitQuantity"> <span> (.*?)</span>', 29, 7).strip(),
                "price_unit_info": None,
                "price_unit_info_unit_size": "",
                "image_url": "http://vomar.nl" + apply_regex(text, 'id="productImage"> <img alt="" src="(.*?)" />', 36, 4).replace("&#47;", "/"),
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
