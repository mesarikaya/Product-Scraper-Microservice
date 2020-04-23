import io
import unittest
from unittest import TestCase
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from products.models import JumboProduct
from products.serializers import JumboProductSerializer
from rest_framework.test import APITestCase


class MyTestCase(APITestCase):

    def setUp(self):
        self.Serializer = JumboProductSerializer
        self.product = JumboProduct(product_id='123512412')
        self.serializer = self.Serializer(self.product)
        self.content = JSONRenderer().render(self.serializer.data)

    def test_serializer(self):
        self.assertTrue(self.serializer.data == {'product_id': '123512412'})
        self.assertTrue(self.content == b'{"product_id":"123512412"}')

    def test_deserialize(self):
        self.assertTrue(self.serializer.data == {'product_id': '123512412'})

        stream = io.BytesIO(self.content)
        data = JSONParser().parse(stream)
        serializer2 = JumboProductSerializer(data=data)

        self.assertTrue(serializer2.is_valid())
        self.assertTrue(len(serializer2.validated_data) == 1)
        self.assertIsInstance(serializer2.save(), JumboProduct)

        retrievedValue = JumboProduct.objects.filter(product_id='123512412')
        self.assertTrue(retrievedValue.count() == 1)


if __name__ == '__main__':
    unittest.main()
