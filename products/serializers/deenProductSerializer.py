from django.utils import timezone
from rest_framework import serializers
from products.models import DeenProduct


class DeenProductSerializer(serializers.Serializer):
    product_id = serializers.CharField(max_length=100, required=True)

    def create(self, validated_data):
        """
        Create and return a new `DeenProduct` instance, given the validated resources.
        """
        return DeenProduct.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `DeenProduct` instance, given the validated resources.
        """
        instance.product_id = validated_data.get('product_id', instance.product_id)
        instance.save()
        return instance
