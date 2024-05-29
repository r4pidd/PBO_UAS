from rest_framework import serializers
from pbo_uas.models import Sale, SaleDetails, Product

class SaleDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetails
        fields = ['payment_method', 'date']


class SaleDetailSerializer(serializers.ModelSerializer):
    note = serializers.CharField(required=False, allow_null=True, allow_blank=True)  # Optional field
    product_category_id = serializers.IntegerField(required=False, allow_null=True)  # Optional field
    product_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)  # Optional field

    class Meta:
        model = SaleDetails
        # Exclude sale_id, product_name, and product_category_id
        fields = ['product_id', 'product_category_id', 'product_name', 'sold_for', 'quantity', 'note']

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

    def update(self, instance, validated_data):
        product_id = validated_data.get('product_id', instance.product_id)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f"Product with id {product_id} does not exist.")

        instance.product_id = product_id
        instance.product_name = product.name
        instance.product_category_id = product.category_id
        instance.sold_for = validated_data.get('sold_for', instance.sold_for)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.note = validated_data.get('note', instance.note)

        instance.save()
        return instance


class SaleSerializer(serializers.ModelSerializer):
    details = SaleDetailSerializer(many=True)
    sale_no = serializers.CharField(required=False, allow_null=True, allow_blank=True)  # Optional field
    paid = serializers.IntegerField(required=False, allow_null=True)  # Optional field
    change = serializers.IntegerField(required=False, allow_null=True)  # Optional field
    total_amount = serializers.IntegerField(required=False, allow_null=True)  # Optional field

    class Meta:
        model = Sale
        fields = ['id', 'sale_no', 'date', 'paid', 'payment_method', 'change', 'total_amount', 'details']

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        sale = Sale.objects.create(**validated_data)
        for detail_data in details_data:
            detail_data['sale_id'] = sale.id
            SaleDetailSerializer().create(detail_data)
        return sale


class GetSaleSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id', 'sale_no', 'date', 'paid', 'payment_method', 'change', 'total_amount', 'details']

    def get_details(self,obj):
        sale_details = SaleDetails.objects.filter(sale_id=obj.id)
        return SaleDetailSerializer(sale_details, many=True).data

