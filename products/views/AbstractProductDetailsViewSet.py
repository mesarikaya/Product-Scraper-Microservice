from abc import abstractmethod
from django.db.models import QuerySet
from rest_framework.views import APIView


class AbstractProductDetailsViewSet(APIView):
    """Enable CRUD operations for AH Products Details Table from retrieved API call JSON resources"""

    def __init__(self):
        super()
        self.product_details = list()

    @abstractmethod
    def get(self):
        """Get all details of all products"""
        """TODO: Create a specific view for admin and other users."""
        """TODO: Create a specific product item search."""
        pass

    @abstractmethod
    def post(self, request, format=None):
        pass

    @staticmethod
    def get_product_id(product_id_list):
        if isinstance(product_id_list, QuerySet) or isinstance(product_id_list, set) or isinstance(product_id_list,list):
            for product_id in product_id_list:
                yield product_id
        else:
            raise TypeError("Parameter for Product Id List is not a Query Set Object")

    @staticmethod
    @abstractmethod
    def get_json_data(product_id):
        pass

    @staticmethod
    @abstractmethod
    def map_product_details(json_value):
        pass

