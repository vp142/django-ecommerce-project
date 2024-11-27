# from django.urls import path
# from . import views

# urlpatterns = [
#     path('dashboard/', views.seller_dashboard, name='seller_dashboard'),
#     path('product/add/', views.add_product, name='add_product'),
#     path('product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
#     path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
# ]

from django.urls import path
from . import views

app_name = 'sellers'

urlpatterns = [
    path('dashboard/', views.seller_dashboard, name='dashboard'),  # Optional: Redirect to products app dashboard
]
