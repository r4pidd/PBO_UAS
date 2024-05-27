from rest_framework import serializers
from pbo_uas.models import Sale, SaleDetails

class SaleDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleDetails
        fields = '__all__'


class SaleSerializer(serializers.ModelSerializer):
    details = SaleDetailsSerializer(many=True)  # Nested serializer for sale details

    class Meta:
        model = Sale
        fields = ['id', 'date', 'payment_method', 'total_amount']

    def create(self, validated_data):
        details_data = validated_data.pop('details')
        sale = Sale.objects.create(**validated_data)
        for detail_data in details_data:
            SaleDetails.objects.create(sale_id=sale.id, **detail_data)
        return sale
