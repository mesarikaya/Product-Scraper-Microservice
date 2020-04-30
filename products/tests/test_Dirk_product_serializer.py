import io
import unittest
from unittest import TestCase
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from products.models import DirkProduct
from products.serializers import DirkProductSerializer
from rest_framework.test import APITestCase


class MyTestCase(APITestCase):

    def setUp(self):
        self.Serializer = DirkProductSerializer
        self.product = DirkProduct(product_id=123512412, category='', product_url="//test")
        self.serializer = self.Serializer(self.product)
        self.content = JSONRenderer().render(self.serializer.data)

    def test_serializer(self):
        print(self.serializer.data)
        self.assertTrue(self.serializer.data == {'product_id': 123512412, 'category': '', 'product_url': '//test'})
        print(self.content)
        self.assertTrue(self.content == b'{"product_id":123512412,"category":"","product_url":"//test"}')

    def test_deserialize(self):
        print(self.serializer.data)
        self.assertTrue(self.serializer.data == {'product_id': 123512412, 'category': '', 'product_url': '//test'})

        stream = io.BytesIO(self.content)
        data = JSONParser().parse(stream)
        serializer2 = DirkProductSerializer(data=data)

        if not serializer2.is_valid():
            print("Serializer is invalid with errors:", serializer2.errors)
        self.assertTrue(serializer2.is_valid())
        self.assertTrue(len(serializer2.validated_data) == 3)
        self.assertIsInstance(serializer2.save(), DirkProduct)

        retrievedValue = DirkProduct.objects.filter(product_id=123512412)
        self.assertTrue(retrievedValue.count() == 1)


if __name__ == '__main__':
    unittest.main()
