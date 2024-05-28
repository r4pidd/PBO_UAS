from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.getSale, name='sale_list'),
    # path('/<int:id>', views.getSaleById, name='sale_by_id'),
    path('/add', views.addSale, name='add_sale'),
    # path('/update', views.updateSale, name='update'),
    # path('/delete/<int:id>', views.deleteSale, name='delete'),
]
