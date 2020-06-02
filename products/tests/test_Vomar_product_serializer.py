import io
import unittest
from unittest import TestCase
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from products.models import VomarProduct
from products.serializers import VomarProductSerializer
from rest_framework.test import APITestCase


class MyTestCase(APITestCase):

    def setUp(self):
        self.Serializer = VomarProductSerializer
        self.product = VomarProduct(product_id='123512412', category="test")
        self.serializer = self.Serializer(self.product)
        self.content = JSONRenderer().render(self.serializer.data)

    def test_serializer(self):
        self.assertTrue(self.serializer.data == {'product_id': '123512412', 'category': 'test'})
        print(self.content)
        self.assertTrue(self.content == b'{"product_id":"123512412","category":"test"}')

    def test_deserialize(self):
        self.assertTrue(self.serializer.data == {'product_id': '123512412', 'category': 'test'})

        stream = io.BytesIO(self.content)
        data = JSONParser().parse(stream)
        serializer2 = VomarProductSerializer(data=data)

        self.assertTrue(serializer2.is_valid())
        self.assertTrue(len(serializer2.validated_data) == 2)
        self.assertIsInstance(serializer2.save(), VomarProduct)

        retrievedValue = VomarProduct.objects.filter(product_id='123512412')
        self.assertTrue(retrievedValue.count() == 1)


if __name__ == '__main__':
    unittest.main()
