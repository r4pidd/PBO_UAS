from rest_framework import serializers
from pbo_uas.models import Sale, SaleDetails, Product

class SaleDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetails
        fields = ['payment_method', 'date']


class SaleDetailSerializer(serializers.ModelSerializer):
    note = serializers.CharField(required=False, allow_null=True, allow_blank=True)  # Optional field

    class Meta:
        model = SaleDetails
        # Exclude sale_id, product_name, and product_category_id
        fields = ['product_id', 'sold_for', 'quantity', 'note']

    def create(self, validated_data):
        product_id = validated_data['product_id']
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f"Product with id {product_id} does not exist.")

        print(f"Product fetched successfully: {product}")
        print(f"Product category_id: {product.category_id}")

        validated_data['product_name'] = product.name
        validated_data['product_category_id'] = product.category_id

        return super().create(validated_data)


class SaleSerializer(serializers.ModelSerializer):
    details = SaleDetailSerializer(many=True)

    class Meta:
        model = Sale
        fields = ['id', 'date', 'payment_method', 'details']

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        sale = Sale.objects.create(**validated_data)
        for detail_data in details_data:
            detail_data['sale_id'] = sale.id
            SaleDetailSerializer().create(detail_data)
        return sale
