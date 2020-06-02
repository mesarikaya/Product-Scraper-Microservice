import json
import logging
from collections import defaultdict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import DirkProduct
from products.serializers import DirkProductSerializer


class DirkProductView(APIView):
    """Enable CRUD operations for Dirk Products Table from scraped JSON resources"""

    def get(self):
        DirkProduct.objects.all()

    def post(self, request, format=None):
        logging.debug("Request body has the following resources: ", request.data, request.data['is_allowed'])
        if request.data['is_allowed']:
            with open('resources/data/dirk_product_ids.json', errors='ignore') as data_file:
                data = data_file.read()
                data = "[" + data + "]"
                data = data.replace("}{", "}, {")
                data = data.replace(",]", "]")
                json_data = json.loads(data, strict=False)

                product_values = defaultdict()
                for item in json_data:
                    product_values.setdefault(item['product_id'], item['category'])

                base_url = "https://www.dirk.nl"
                data_to_serialize = list()
                for product, category in product_values.items():
                    product_url = base_url + product
                    product_id = DirkProductView.retrieve_product_id(product)
                    data_to_serialize.append({'product_id': product_id,
                                              'product_url': product_url,
                                              'category': category})

                serializer = DirkProductSerializer(data=data_to_serialize, many=True)
                if serializer.is_valid():
                    try:
                        logging.debug("Saving with serializer")
                        instance = serializer.save()
                    except Exception as e:
                        logging.debug("Error in serialize.save() for batch product id load.")

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                logging.debug("Serializer is invalid with errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)

    @staticmethod
    def retrieve_product_id(json_value):
        try:
            string_parts = json_value.split('/')
        except IndexError as e:
            logging.debug("Index Error: ", e)
        except Exception as e:
            logging.debug("Exception: ", e)
        else:
            return getID(string_parts)


def getID(string_parts):
    try:
        result = int(string_parts[len(string_parts) - 1])
    except Exception as e:
        return -1
    else:
        return result

