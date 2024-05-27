from rest_framework import serializers
from sales.models import Product, ProductCategory

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
