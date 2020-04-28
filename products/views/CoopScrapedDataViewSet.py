import json
import logging
from collections import defaultdict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import CoopProduct

from products.serializers import CoopProductSerializer


class CoopProductView(APIView):
    """Enable CRUD operations for Jumbo Products Table from scraped JSON resources"""

    def get(self):
        CoopProduct.objects.all()

    def post(self, request, format=None):
        logging.debug("Request body has the following resources: ", request.data, request.data['is_allowed'])
        if request.data['is_allowed']:
            with open('resources/data/coop_product_ids.json', errors='ignore') as data_file:
                data = data_file.read()
                data = "[" + data + "]"
                data = data.replace("}{", "}, {")
                data = data.replace(",]", "]")
                json_data = json.loads(data, strict=False)

                product_values = defaultdict()
                for item in json_data:
                    product_values.setdefault(item['product_id'], item['category'])

                data_to_serialize = list()
                for product, category in product_values.items():
                    product_url = product
                    product_id = CoopProductView.retrieve_product_id(product)
                    data_to_serialize.append({'product_id': product_id,
                                              'product_url': product_url,
                                              'category': category})
                    print("Product item values: product:", product_id,
                          "and category:", category,
                          "and url:", product_url)

                serializer = CoopProductSerializer(data=data_to_serialize, many=True)
                if serializer.is_valid():
                    try:
                        logging.debug("Saving with serializer")
                        instance = serializer.save()
                    except Exception as e:
                        logging.debug("Error in serialize.save() for batch product id load.")
                        raise IOError from e

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                print("Serializer is invalid with errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)

    @staticmethod
    def retrieve_product_id(json_value):
        try:
            string_parts = json_value.split('/')
        except IndexError as e:
            print("Index Error: ", e)
        except Exception as e:
            print("Exception: ", e)
        else:
            return int(string_parts[len(string_parts) - 1])
