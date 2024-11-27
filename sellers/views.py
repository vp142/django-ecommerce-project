# from django.shortcuts import render, get_object_or_404, redirect
# from django.contrib.auth.decorators import login_required
# from django.http import HttpResponseForbidden
# from products.models import Product
# from .models import Seller
# from products.forms import ProductForm

# def seller_required(view_func):
#     """Decorator to restrict access to sellers only."""
#     def _wrapped_view_func(request, *args, **kwargs):
#         if not request.user.is_authenticated or not request.user.is_seller:
#             return HttpResponseForbidden("You are not allowed to access this page.")
#         return view_func(request, *args, **kwargs)
#     return _wrapped_view_func

# @seller_required
# def seller_dashboard(request):
#     """View for seller to see their products."""
#     seller = get_object_or_404(Seller, user=request.user)
#     products = Product.objects.filter(seller=seller)
#     return render(request, '/sellers/dashboard.html', {'products': products})

# @seller_required
# def add_product(request):
#     """View for seller to add a new product."""
#     seller = get_object_or_404(Seller, user=request.user)
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES)
#         if form.is_valid():
#             product = form.save(commit=False)
#             product.seller = seller
#             product.save()
#             return render(request, 'sellers/dashboard.html',)
#     else:
#         form = ProductForm()
#     return render(request, 'sellers/add_product.html', {'form': form})

# @seller_required
# def edit_product(request, product_id):
#     """View for seller to edit an existing product."""
#     seller = get_object_or_404(Seller, user=request.user)
#     product = get_object_or_404(Product, id=product_id, seller=seller)
#     if request.method == 'POST':
#         form = ProductForm(request.POST, request.FILES, instance=product)
#         if form.is_valid():
#             form.save()
#             return redirect('seller_dashboard')
#     else:
#         form = ProductForm(instance=product)
#     return render(request, 'sellers/edit_product.html', {'form': form, 'product': product})

# @seller_required
# def delete_product(request, product_id):
#     """View for seller to delete a product."""
#     seller = get_object_or_404(Seller, user=request.user)
#     product = get_object_or_404(Product, id=product_id, seller=seller)
#     if request.method == 'POST':
#         product.delete()
#         return redirect('seller_dashboard')
#     return render(request, 'sellers/delete_product.html', {'product': product})
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
@login_required
def seller_dashboard(request):
    """Redirect to the products app seller dashboard."""
    return redirect('products:seller_dashboard')
