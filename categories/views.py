from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from sales.models import ProductCategory
from categories.serializers import CategorySerializer
from sales.response import ok_with_msg, ok_with_data, error_with_msg, error_with_data


@api_view(['GET'])
def getCategory(request):
    name = request.query_params.get('name', None)

    # get all the data from db
    categories = ProductCategory.objects.all()

    # filter
    if name:
        categories = categories.filter(name__icontains=name)

    # serialize and return it
    serializer = CategorySerializer(categories, many=True)
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
    category_id = request.data.get('id')
    if not category_id:
        return error_with_msg(msg='id is required!')

    # check if the category exists
    category = get_object_or_404(ProductCategory, pk=category_id)

    # delete the category
    category.delete()

    return ok_with_msg(msg='category deleted successfully!')
