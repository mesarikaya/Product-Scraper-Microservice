from rest_framework import serializers
from products.models import AlbertHeijnProductDetails
from products.serializers import BaseProductDetailsSerializer


class AlbertHeijnProductDetailsSerializer(BaseProductDetailsSerializer):
    product_id = serializers.IntegerField(required=True)

    def create(self, validated_data):
        """
        Create and return a new `AlbertHeijnProductDetails` instance, given the validated resources.
        """
        return AlbertHeijnProductDetails.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `AlbertHeijnProductDetails` instance, given the validated resources.
        """
        instance.product_id = validated_data.get('product_id', instance.product_id)
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.summary = validated_data.get('summary', instance.summary)
        instance.is_available = validated_data.get('is_available', instance.is_available)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.price_now = validated_data.get('price_now', instance.price_now)
        instance.price_now_unit_size = validated_data.get('price_now_unit_size', instance.price_now_unit_size)
        instance.price_unit_info = validated_data.get('price_unit_info', instance.price_unit_info)
        instance.price_unit_info_unit_size = validated_data.get('price_unit_info_unit_size',
                                                                instance.price_unit_info_unit_size)
        instance.catalog_id = validated_data.get('catalog_id', instance.catalog_id)
        instance.brand = validated_data.get('brand', instance.brand)
        instance.category = validated_data.get('category', instance.category)
        instance.hq_id = validated_data.get('hq_id', instance.hq_id)
        instance.is_medicine = validated_data.get('is_medicine', instance.is_medicine)
        instance.properties = validated_data.get('properties', instance.properties)
        instance.save()
        return instance
