from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.homeView, name='home'),
    path('customer/<str:user_id>/',views.customerView, name='customer'),
    path('products/', views.productsView, name='products'),
    path('create/customer/', views.createCustomerView, name='createcustomer'),
    path('create/order/', views.createOrderView, name='createorder'),
    path('update/order/<str:order_id>/', views.orderUpdateView, name='updateorder'),
    path('delete/order/<str:order_id>/', views.orderDeleteView, name='deleteorder'),
]


