from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from pbo_uas.models import ProductCategory
from categories.serializers import CategorySerializer
from pbo_uas.response import ok_with_msg, ok_with_data, error_with_msg


@api_view(['GET'])
def getCategory(request):
    # get all the data from db
    products = ProductCategory.objects.all()

    # serialize and return it
    serializer = CategorySerializer(products, many=True)
    return ok_with_data(data=serializer.data, msg='ok')


@api_view(['POST'])
def addCategory(request):
    # get the data
    serializer = CategorySerializer(data=request.data)

    # check is the requested data valid
    if serializer.is_valid():
        serializer.save()
        return ok_with_msg(msg='category created successfully!')
    else:
        return error_with_msg(msg=serializer.errors)


@api_view(['POST'])
def updateCategory(request):
    # get id
    category_id = request.data.get('id')
    if not category_id:
        return error_with_msg(msg='id is required!')

    # check the data is exist
    category = get_object_or_404(ProductCategory, pk=category_id)

    # get the data
    serializer = CategorySerializer(category, data=request.data, partial=True if request.method == 'PATCH' else False)

    # check is the requested data valid
    if serializer.is_valid():
        serializer.save()
        return ok_with_msg(msg='category updated successfully!')
    else:
        return error_with_msg(msg=serializer.errors)


@api_view(['DELETE'])
def deleteCategory(request):
    # get id
    product_id = request.data.get('id')
    if not product_id:
        return error_with_msg(msg='id is required!')

    # check if the product exists
    product = get_object_or_404(ProductCategory, pk=product_id)

    # delete the product
    product.delete()

    return ok_with_msg(msg='category deleted successfully!')
