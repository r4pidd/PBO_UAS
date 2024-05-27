from django.shortcuts import get_object_or_404
from pbo_uas.models import Product,ProductCategory
from django.http import JsonResponse

# Create your views here.
def index(request):
    return JsonResponse("Hello, world!")

def product_index(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category_id')
        desc = request.POST.get('desc')
        image_path = request.POST.get('image_path')
        price = request.POST.get('price')

        if name and category_id:
            product = Product(name=name, category_id=category_id, desc=desc, image_path=image_path, price=price)
            product.save()
            return JsonResponse({
                "message": "Product saved",
                "success": 1
            })
        else:
            return JsonResponse({
                "message": "Name and Category is required",
                "success": 0
            })

    else:
        return JsonResponse({
            "products": Product.objects.all(),
            "categories": ProductCategory.objects.all()
        })

def product_details(request, id):
    return JsonResponse({
        "product": get_object_or_404(Product, pk=id)
    })

# def product_create(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category_id')
        desc = request.POST.get('desc')
        image_path = request.POST.get('image_path')
        price = request.POST.get('price')

        if name and category_id:
            product = Product(name=name, category_id=category_id, desc=desc, image_path=image_path, price=price)
            product.save()
            return JsonResponse({
                "message": "Product saved",
                "success": 1
            })
        else:
            return JsonResponse({
                "message": "Name and Category is required",
                "success": 0
            })


    return JsonResponse({
        "message": "Wrong method passed",
        "success": 0
    })


def product_update(request, id):
    product = get_object_or_404(Product, pk=id)

    if request.method == 'POST':
        name = request.POST.get('name')
        category_id = request.POST.get('category_id')
        desc = request.POST.get('desc')
        image_path = request.POST.get('image_path')
        price = request.POST.get('price')


        if name and category_id:
            product.name = name
            product.category_id = category_id
            product.desc = desc
            product.image_path = image_path
            product.price = price
            product.save()
            return JsonResponse({
                "message": "Product updated successfully",
                "success": 1
            })
        else:
            return JsonResponse({
                "message": "Name and Category is required",
                "success": 0
            })

    return JsonResponse({
        "message": "Wrong method passed",
        "success": 0
    })
