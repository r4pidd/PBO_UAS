from django.urls import path, include
from products import views

urlpatterns = [
    path('', views.getProduct, name='product_list'),
    path('/<int:id>', views.getProductById, name='product_by_id'),
    path('/add', views.addProduct, name='add_product'),
    path('/update', views.updateProduct, name='update_product'),
    path('/delete', views.deleteProduct, name='delete_product')
]
