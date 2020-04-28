import json
import logging

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from products.models import JumboProduct
from products.serializers import JumboProductSerializer


class JumboProductView(APIView):
    """Enable CRUD operations for Jumbo Products Table from scraped JSON resources"""

    def get(self):
        JumboProduct.objects.all()

    def post(self, request, format=None):
        logging.debug("Request body has the following resources: ", request.data, request.data['is_allowed'])
        if request.data['is_allowed']:
            with open('resources/data/jumbo_product_ids.json', errors='ignore') as data_file:
                data = data_file.read()
                data = "[" + data + "]"
                data = data.replace("}{", "}, {")
                data = data.replace(",]", "]")
                json_data = json.loads(data, strict=False)

                values = set()
                for item in json_data:
                    values.add(item['product_id'])

                data_to_serialize = list()
                for i in values:
                    data_to_serialize.append({'product_id': i})

                serializer = JumboProductSerializer(data=data_to_serialize, many=True)
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
