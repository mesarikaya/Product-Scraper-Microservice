from django.utils import timezone
from rest_framework import serializers

from products.models import AlbertHeijnProduct


class AlbertHeijnProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)

    def create(self, validated_data):
        """
        Create and return a new `AlbertHeijnProduct` instance, given the validated resources.
        """
        return AlbertHeijnProduct.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `AlbertHeijnProduct` instance, given the validated resources.
        """
        instance.product_id = validated_data.get('product_id', instance.product_id)
        instance.save()
        return instance
