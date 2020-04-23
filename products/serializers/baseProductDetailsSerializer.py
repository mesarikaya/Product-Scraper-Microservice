from rest_framework import serializers
from products.models import AlbertHeijnProductDetails


class BaseProductDetailsSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
    title = serializers.CharField(required=False, max_length=200, allow_blank=True)
    description = serializers.CharField(required=False, allow_blank=True)
    summary = serializers.CharField(required=False, max_length=10000, allow_blank=True)
    is_available = serializers.BooleanField(required=False, default=True)
    image_url = serializers.CharField(required=False, max_length=250, allow_blank=True)
    price_now = serializers.DecimalField(required=False, max_digits=10, decimal_places=4, allow_null=True)
    price_now_unit_size = serializers.CharField(required=False, max_length=50, allow_blank=True)
    price_unit_info = serializers.DecimalField(required=False, max_digits=10, decimal_places=4, allow_null=True)
    price_unit_info_unit_size = serializers.CharField(required=False, max_length=50, allow_blank=True)
    catalog_id = serializers.IntegerField(required=False, allow_null=True)
    brand = serializers.CharField(required=False, max_length=200, allow_blank=True)
    category = serializers.CharField(required=False, max_length=200, allow_blank=True)
    hq_id = serializers.IntegerField(allow_null=True)
    is_medicine = serializers.BooleanField(allow_null=True)
    properties = serializers.CharField(allow_blank=True)

    def create(self, validated_data):
        """
        abstract create method
        """
        pass

    def update(self, instance, validated_data):
        """
        abstract update method
        """
        pass
