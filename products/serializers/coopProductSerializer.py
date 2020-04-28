from django.utils import timezone
from rest_framework import serializers
from products.models import CoopProduct


class CoopProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    category = serializers.CharField(max_length=200, required=False, allow_blank=True)
    product_url = serializers.CharField(max_length=500, required=True, allow_blank=False)

    def create(self, validated_data):
        """
        Create and return a new `JumboProduct` instance, given the validated resources.
        """
        return CoopProduct.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `JumboProduct` instance, given the validated resources.
        """
        instance.product_id = validated_data.get('product_id', instance.product_id)
        instance.product_url = validated_data.get('product_url', instance.product_url)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance
