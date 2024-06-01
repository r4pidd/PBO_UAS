from django.urls import path, include
from . import views

urlpatterns = [
    path('/predict', views.pred_qty, name='sale_list'),
]
