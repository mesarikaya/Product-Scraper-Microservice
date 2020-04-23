import logging
import random
import requests
import re
import json

from datetime import timedelta
from background_task import background
from django.utils import timezone
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import JumboProductDetails
from products.serializers import JumboProductDetailsSerializer
from products.models import JumboProduct
from decimal import Decimal


class JumboProductDetailsViewSet(APIView):
    """Enable CRUD operations for AH Products Details Table from retrieved API call JSON resources"""

    def __init__(self):
        super()
        self.product_details = list()

    def get(self):
        """Get all details of all products"""
        """TODO: Create a specific view for admin and other users."""
        """TODO: Create a specific product item search."""
        JumboProductDetails.objects.all()

    def post(self, request, format=None):
        # logging.debug("Request body has the following resources: ", request.resources, request.resources['is_allowed'])
        """TODO: Create an env variable for this url"""
        batch_size = request.data['batch_size']
        is_allowed = request.data['is_allowed']
        if is_allowed and batch_size >= 0 and batch_size:
            try:
                # .filter(product_id=476347)
                product_id_list = list(set(list(JumboProduct.objects.values_list('product_id', flat=True))))
                batchStart = 0
                batchEnd = 0
                total_product_count = len(product_id_list)
                while batchStart < total_product_count:
                    batchStart = batchEnd
                    batchEnd = batchStart + batch_size
                    if batchEnd > total_product_count:
                        batchEnd = total_product_count

                    if batchStart == total_product_count:
                        break

                    time_delay_in_seconds = random.randint(3, 7)
                    next_run = timezone.now() + timedelta(seconds=time_delay_in_seconds)
                    JumboProductDetailsViewSet \
                        .create_product_details(product_id_list, batchStart, batchEnd, schedule=time_delay_in_seconds,
                                                verbose_name='get_Jumbo_Product_details' + "-" + str(next_run))
                return Response("Success", status=status.HTTP_201_CREATED)
            except Exception as e:
                raise Exception(e)
                return Response("Error in execution", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied", status=status.HTTP_400_BAD_REQUEST)

        return Response("Success", status=status.HTTP_201_CREATED)

    @staticmethod
    @background(schedule=5)
    def create_product_details(ids, start, end):
        print("Start:", start, "End:", end)
        product_id_list = ids[start:end]
        data = list()
        logging.info("Running for start:", start, "End:", end)
        for product_id in JumboProductDetailsViewSet.get_product_id(product_id_list):
            result = JumboProductDetailsViewSet.get_json_data(product_id)
            if result:
                data.append(result)

        serializer = JumboProductDetailsSerializer(data=data, many=True)
        if serializer.is_valid():
            try:
                logging.debug("Saving with serializer")
                serializer.save()
            except Exception as e:
                logging.info("Error in serialize.save() for batch product id load.")
                raise IOError(e)
        else:
            print("Serializer is invalid with errors:", serializer.errors)

    @staticmethod
    def get_product_id(product_id_list):
        if isinstance(product_id_list, QuerySet) or isinstance(product_id_list, set) or isinstance(product_id_list,
                                                                                                   list):
            for product_id in product_id_list:
                yield product_id
        else:
            raise TypeError("Parameter for Product Id List is not a Query Set Object")

    @staticmethod
    def get_json_data(product_id):
        """TODO: Create an env variable for this url"""
        base_url = 'https://www.jumbo.com'
        headers = {'User-agent': 'PostmanRuntime/7.24.0'}
        print("Searching product id:", product_id)
        try:
            r = requests.get(url=base_url + product_id, headers=headers)
            text = r.content.decode("utf-8")
            result = JumboProductDetailsViewSet.map_product_details(text)
            return result
        except Exception as e:
            raise Exception(e)
        else:
            return result

    @staticmethod
    def map_product_details(text):
        try:
            try:
                general_price_info = apply_regex(text, 'jum-comparative-price">((.*?))</span>', 24, 8).replace("&#47;",
                                                                                                               ";")
                # print("General_price_info:", general_price_info)
                price_unit_info = Decimal(general_price_info.split(";")[0].replace(',', '.'))
                price_unit_info_unit_size = general_price_info.split(";")[1]
            except Exception as e:
                # print("Error in getting general price info: ", e)
                price_unit_info = None
                price_unit_info_unit_size = ""

            data = {
                "description": apply_regex(text, '<h3>Productomschrijving</h3>(.*?)</div>', 28, 6)[:100],
                "price_now_unit_size": apply_regex(text, 'jum-pack-size">(.*?)</span>', 15, 7),
                "price_unit_info": price_unit_info,
                "price_unit_info_unit_size": price_unit_info_unit_size,
                "image_url": apply_regex(text, 'resources-jum-hr-src="(.*?)"', 17, 1).replace("&#47;", "/"),
                "summary": apply_regex(text, '<div class="jum-summary-description">\n<p>(.*?)</p>', 41, 4),
                "hq_id": None,
                "properties": "",
                "is_medicine": None
            }
            product_details = clean_product_details(apply_regex(text, 'resources-jum-product-details="(.*?)"', 26, 1))
            print("Product details: ", product_details)
            data.setdefault('title', product_details.get('name', ""))
            data.setdefault('price_now', product_details.get('price', None))
            data.setdefault('brand', product_details.get('brand', ""))
            data.setdefault('category', product_details.get('category', ""))
            data.setdefault('product_id', product_details.get('id', "-1"))
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


# Helper functions
def apply_regex(text, regex, offset_left, offset_right):
    try:
        match = re.search(regex, text)
        start = int(match.start()) + offset_left
        end = int(match.end()) - offset_right
    except IndexError as e:
        print("Error with start and stop indices:", e)
        return ""
    except Exception as e:
        # print("Exception in searching text:", e)
        return ""
    else:
        return text[start:end]


def clean_product_details(text):
    try:
        result = json.loads(text
                            .replace("&quot;", "\"")
                            .replace("\\", "")
                            .replace("&#47;", "-"))
    except Exception as e:
        print("Exception during json load:", e)
        return {'name': '', 'id': "-1", 'price': None, 'brand': '', 'category': ''}
    else:
        return result
