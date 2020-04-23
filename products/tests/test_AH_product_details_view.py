import io
import unittest

from django.urls import include, path
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from products.models import AlbertHeijnProductDetails
from products.serializers import AlbertHeijnProductDetailsSerializer
from rest_framework.response import Response
from rest_framework.test import APIClient, APITestCase, URLPatternsTestCase


class AHProductDetailsViewTest(APITestCase):

    def setUp(self):
        self.client = APIClient()
        print("Initially, all items in the database: ", AlbertHeijnProductDetails.objects.all())

    def test_data_load(self):
        response = self.client.post('/products/api/v1/get/details', data={'is_allowed': True}, format='json')

        self.assertIsInstance(response, Response)
        self.assertTrue(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(len(response.items()) > 0)


if __name__ == '__main__':
    unittest.main()
