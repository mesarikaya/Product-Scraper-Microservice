import logging
import random
import requests

from datetime import timedelta
from background_task import background
from django.utils import timezone
from collections import defaultdict
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import AlbertHeijnProductDetails
from products.serializers import AlbertHeijnProductDetailsSerializer
from products.models import AlbertHeijnProduct


class AHProductDetailsViewSet(APIView):
    """Enable CRUD operations for AH Products Details Table from retrieved API call JSON resources"""

    def __init__(self):
        super()
        self.product_details = list()

    def get(self):
        """Get all details of all products"""
        """TODO: Create a specific view for admin and other users."""
        """TODO: Create a specific product item search."""
        AlbertHeijnProductDetails.objects.all()

    def post(self, request, format=None):
        # logging.debug("Request body has the following resources: ", request.resources, request.resources['is_allowed'])
        batch_size = request.data['batch_size']
        is_allowed = request.data['is_allowed']
        if is_allowed and batch_size >= 0 and batch_size:
            try:
                # .filter(product_id=476347)
                product_id_list = list(set(list(AlbertHeijnProduct.objects.values_list('product_id', flat=True))))
                print("Length of product list: ", len(product_id_list))
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

                    time_delay_in_seconds = random.randint(1, 5)
                    next_run = timezone.now() + timedelta(seconds=time_delay_in_seconds)
                    AHProductDetailsViewSet.create_product_details(product_id_list,
                                                                   batchStart,
                                                                   batchEnd,
                                                                   schedule=time_delay_in_seconds,
                                                                   verbose_name='get_AH_product_details'
                                                                                + "-"
                                                                                + str(next_run))
                return Response("Success", status=status.HTTP_201_CREATED)
            except Exception as e:
                raise Exception(e)
                return Response("Error in execution", status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied", status=status.HTTP_400_BAD_REQUEST)

    @staticmethod
    @background(schedule=5)
    def create_product_details(ids, start, end):
        print("Start:", start, "End:", end)
        product_id_list = ids[start:end]
        data = list()
        logging.info("Running for start:", start, "End:", end)
        for product_id in AHProductDetailsViewSet.get_product_id(product_id_list):
            result = AHProductDetailsViewSet.get_json_data(product_id)
            if result:
                data.append(result)

        serializer = AlbertHeijnProductDetailsSerializer(data=data, many=True)
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
        if isinstance(product_id_list, QuerySet) or isinstance(product_id_list, set) or isinstance(product_id_list,list):
            for product_id in product_id_list:
                yield product_id
        else:
            raise TypeError("Parameter for Product Id List is not a Query Set Object")

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
            return result
        except Exception as e:
            raise Exception(e)
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
            raise KeyError(e)
        except IndexError as e:
            logging.debug("Index Error: ", e)
            print("Index error: ", json_value)
            raise IndexError(e, json_value)
        except Exception as e:
            logging.debug("Exception: ", e, json_value)
            raise Exception(e)
        else:
            return data
