from django.urls import path
from . import views
# from .views import get_products

app_name = 'products'

urlpatterns = [
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/cancel/', views.payment_cancel, name='payment_cancel'),
    path('all/', views.all_products, name='all_products'),
    path('seller/dashboard/', views.seller_dashboard, name='seller_dashboard'),
    path('seller/products/add/', views.add_product, name='add_product'),
    path('seller/products/edit/<int:product_id>/', views.edit_product, name='edit_product'),
    path('seller/products/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('cart/checkout/', views.create_checkout_session, name='create_checkout_session'),
    path('cart/success/', views.payment_success, name='payment_success'),
    path('cart/cancel/', views.payment_cancel, name='payment_cancel'),
    path('orders/', views.user_orders, name='user_orders'),  # For users
    path('seller/orders/', views.seller_orders, name='seller_orders'),
    # path('api/products/', get_products, name='get_products'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),


]
