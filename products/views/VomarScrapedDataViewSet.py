import json
import logging
from collections import defaultdict

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import VomarProduct
from products.serializers import VomarProductSerializer


class VomarProductView(APIView):
    """Enable CRUD operations for Dirk Products Table from scraped JSON resources"""

    def get(self):
        VomarProduct.objects.all()

    def post(self, request, format=None):
        logging.debug("Request body has the following resources: ", request.data, request.data['is_allowed'])
        if request.data['is_allowed']:
            with open('resources/data/vomar_product_ids.json', errors='ignore') as data_file:
                data = data_file.read()
                data = "[" + data + "]"
                data = data.replace("}{", "}, {")
                data = data.replace(",]", "]")
                json_data = json.loads(data, strict=False)

                product_values = defaultdict()
                for item in json_data:
                    product_values.setdefault(item['product_id'], item['category'])

                base_url = "https://www.vomar.nl"
                data_to_serialize = list()
                for product, category in product_values.items():
                    product_url = base_url + product
                    product_id = product_url
                    data_to_serialize.append({'product_id': product_id,
                                              'category': category})

                serializer = VomarProductSerializer(data=data_to_serialize, many=True)
                if serializer.is_valid():
                    try:
                        logging.debug("Saving with serializer")
                        instance = serializer.save()
                    except Exception as e:
                        logging.debug("Error in serialize.save() for batch product id load.")

                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                logging.info("Serializer is invalid with errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("Permission denied", status=status.HTTP_403_FORBIDDEN)

