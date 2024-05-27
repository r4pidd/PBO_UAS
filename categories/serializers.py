from rest_framework import serializers
from sales.models import ProductCategory

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ['id', 'name']
