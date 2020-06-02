from django.utils import timezone
from rest_framework import serializers
from products.models import VomarProduct


class VomarProductSerializer(serializers.Serializer):
    product_id = serializers.CharField(max_length=255, required=True)
    category = serializers.CharField(max_length=200, required=False, allow_blank=True)

    def create(self, validated_data):
        """
        Create and return a new `VomarProduct` instance, given the validated resources.
        """
        return VomarProduct.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `VomarProduct` instance, given the validated resources.
        """
        instance.product_id = validated_data.get('product_id', instance.product_id)
        instance.category = validated_data.get('category', instance.category)
        instance.save()
        return instance
