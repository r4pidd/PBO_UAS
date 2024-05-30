from rest_framework import serializers
from django.db import transaction
from pbo_uas.models import Sale, SaleDetails, Product


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
    age = serializers.IntegerField(required=False, allow_null=True)  # Optional field

    class Meta:
        model = Sale
        fields = ['id', 'sale_no', 'date', 'paid', 'payment_method', 'change', 'total_amount', 'details', 'gender',
                  'age']

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        sale = Sale.objects.create(**validated_data)
        total_amount = 0

        for detail_data in details_data:
            total_amount = total_amount + detail_data['sold_for'] * detail_data['quantity']
            detail_data['sale_id'] = sale.id
            SaleDetailSerializer().create(detail_data)

        sale.total_amount = total_amount
        sale.save()
        return sale


class GetSaleSerializer(serializers.ModelSerializer):
    details = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        fields = ['id', 'sale_no', 'date', 'paid', 'payment_method', 'change', 'total_amount', 'details', 'age',
                  'gender', 'gender_display', 'age_display']
        # fields = '__all__'

    def get_details(self, obj):
        sale_details = SaleDetails.objects.filter(sale_id=obj.id)
        return SaleDetailSerializer(sale_details, many=True).data


class UpdateSaleSerializer(serializers.ModelSerializer):
    details = SaleDetailSerializer(many=True)

    # details = serializers.SerializerMethodField()

    class Meta:
        model = Sale
        # fields = ['id', 'sale_no', 'date', 'paid', 'payment_method', 'change', 'total_amount', 'details']
        fields = ['id', 'sale_no', 'date', 'paid', 'payment_method', 'change', 'total_amount', 'gender', 'age']

    # def get_details(self, obj):
    #     sale_details = SaleDetails.objects.filter(sale_id=obj.id)
    #     return SaleDetailSerializer(sale_details, many=True).data

    def update(self, instance, validated_data):
        print(f"Product category_id:")
        details_data = validated_data.pop('details', None)
        instance.sale_no = validated_data.get('sale_no', instance.sale_no)
        instance.date = validated_data.get('date', instance.date)
        instance.paid = validated_data.get('paid', instance.paid)
        instance.payment_method = validated_data.get('payment_method', instance.payment_method)
        instance.change = validated_data.get('change', instance.change)
        instance.total_amount = validated_data.get('total_amount', instance.total_amount)
        instance.age = validated_data.get('age', instance.age)
        instance.gender = validated_data.get('gender', instance.gender)
        instance.save()
        print(details_data)
        if details_data is not None:
            # Delete existing sale details
            SaleDetails.objects.filter(sale_id=instance.id).delete()
            # Recreate new sale details
            for detail_data in details_data:
                detail_data['sale_id'] = instance.id
                SaleDetailSerializer().create(detail_data)

        return instance
