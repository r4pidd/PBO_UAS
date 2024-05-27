from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from sales.serializers import SaleSerializer
from pbo_uas.models import Sale
from pbo_uas.response import ok_with_msg, ok_with_data, error_with_msg

@api_view(['GET'])
def getSale(request):
    # get all the data from db
    sales = Sale.objects.all()

    # serialize and return it
    serializer = SaleSerializer(sales, many=True)
    return ok_with_data(data=serializer.data, msg='ok')
