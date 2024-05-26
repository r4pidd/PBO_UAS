from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.product_index, name='products.index'),
    path('<int:id>/update/', views.product_update, name='product_update'),
]
