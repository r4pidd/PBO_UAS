from django.urls import path, include
from categories import views

urlpatterns = [
    path('', views.getCategory, name='category_list'),
    path('/<int:id>', views.getCategoryById, name='category_by_id'),
    path('/add', views.addCategory, name='add_category'),
    path('/update', views.updateCategory, name='update'),
    path('/delete', views.deleteCategory, name='delete'),
]
