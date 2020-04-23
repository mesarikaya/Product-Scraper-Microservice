import io
import unittest
from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
from products.models import JumboProductDetails
from products.serializers import JumboProductDetailsSerializer
from rest_framework.test import APITestCase


class MyTestCase(APITestCase):

    def setUp(self):
        self.Serializer = JumboProductDetailsSerializer
        self.product = JumboProductDetails(product_id='123512412')
        self.serializer = self.Serializer(self.product)
        self.content = JSONRenderer().render(self.serializer.data)

    def test_serializer(self):
        self.assertTrue(self.serializer.data['product_id'] == '123512412')

    def test_deserialize(self):
        self.assertTrue(self.serializer.data['product_id'] == '123512412')

        stream = io.BytesIO(self.content)
        data = JSONParser().parse(stream)
        serializer2 = JumboProductDetailsSerializer(data=data)
        self.assertTrue(serializer2.is_valid())
        self.assertTrue(len(serializer2.validated_data) == 16)
        print("Serializer save: ",
              serializer2.save())
        self.assertIsInstance(serializer2.save(), JumboProductDetails)

        retrievedValue = JumboProductDetails.objects.filter(product_id='123512412')
        self.assertTrue(retrievedValue.count() == 1)


if __name__ == '__main__':
    unittest.main()
