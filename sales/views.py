from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from sales.serializers import SaleSerializer, GetSaleSerializer, UpdateSaleSerializer, SaleDetailSerializer
from pbo_uas.models import Sale, SaleDetails
from pbo_uas.response import ok_with_msg, ok_with_data, error_with_msg, error_with_data
from django.utils.dateparse import parse_date
import logging


@api_view(['GET'])
def getSale(request):
    # get all the data from db
    start_date = request.query_params.get('start')
    end_date = request.query_params.get('end')
    order_by = '-date' if request.query_params.get('desc') == 'false' else 'date'

    if start_date and end_date:
        try:
            start_date = parse_date(start_date)
            end_date = parse_date(end_date)
        except ValueError:
            # return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
            return error_with_msg(msg="Invalid date format")

        if not start_date or not end_date:
            # return Response({"error": "Invalid date format"}, status=status.HTTP_400_BAD_REQUEST)
            return error_with_msg(msg="Invalid date format")
        sales = Sale.objects.filter(date__range=(start_date, end_date)).order_by(order_by).all()
    else:
        sales = Sale.objects.order_by(order_by).all()

    serializer = GetSaleSerializer(sales, many=True)
    return ok_with_data(data=serializer.data, msg='ok')


@api_view(['GET'])
def getSaleById(request, id):
    # get all the data from db
    sales = Sale.objects.get(pk=id)
    serializer = GetSaleSerializer(sales, many=False)
    return ok_with_data(data=serializer.data, msg='ok')


@api_view(['POST'])
def addSale(request):
    serializer = SaleSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return ok_with_msg(msg='Sale created successfully!')
    else:
        return error_with_msg(msg=serializer.errors)


@api_view(['POST'])
def updateSale(request):
    sale_id = request.data.get('id')
    sale = Sale.objects.get(pk=sale_id)

    UpdateSaleSerializer.update(sale, instance=sale, validated_data=request.data)

    return ok_with_msg(msg='Sale update successfully!')

    # return ok_with_data(serialized.data, msg='ok')


@api_view(['DELETE'])
def deleteSale(request, id):
    sale = get_object_or_404(Sale, pk=id)

    # delete the product
    SaleDetails.objects.filter(sale_id=id).delete()
    sale.delete()

    return ok_with_msg(msg='Sale deleted successfully!')

