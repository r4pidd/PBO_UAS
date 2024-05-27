from django.urls import path, include
from categories import views

urlpatterns = [
    path('', views.getCategory, name='category_list'),
    path('/add', views.addCategory, name='add_category'),
    path('/update', views.updateCategory, name='update'),
    path('/delete', views.deleteCategory, name='delete'),
]
