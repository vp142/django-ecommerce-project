from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('all/', views.all_products, name='all_products'),
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/products/add/', views.add_product, name='add_product'),
    path('seller/products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('seller/products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
]
