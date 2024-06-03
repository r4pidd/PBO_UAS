from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from sales.serializers import SaleSerializer
from pbo_uas.models import Sale
from pbo_uas.response import ok_with_msg, ok_with_data, error_with_msg

@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def getSale(request):
    # get all the data from db
    sales = Sale.objects.all()

    # serialize and return it
    serializer = SaleSerializer(sales, many=True)
    return ok_with_data(data=serializer.data, msg='ok')
