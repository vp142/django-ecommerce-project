from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product
from sellers.models import Seller
from .forms import ProductForm
from django.http import HttpResponseForbidden

def seller_required(view_func):
    """Decorator to restrict access to sellers only."""
    def _wrapped_view_func(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_seller:
            return HttpResponseForbidden("You are not allowed to access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view_func

@login_required
# def all_products(request):
#     """View for all users to see products."""
#     products = Product.objects.all()
#     return render(request, 'products/all_products.html', {'products': products})

def all_products(request):
    """View to display all products with search, filter, and sort functionality."""
    products = Product.objects.all()

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Filter by price range (optional)
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Sort functionality
    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')

    context = {
        'products': products,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    }
    return render(request, 'products/all_products.html', context)

@seller_required
def seller_dashboard(request):
    """View to display seller's products with search, filter, and sort functionality."""
    seller = request.user.seller_profile
    products = Product.objects.filter(seller=seller)

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = products.filter(name__icontains=search_query)

    # Filter by price range
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)

    # Sort functionality
    sort_by = request.GET.get('sort', '')
    if sort_by == 'price_asc':
        products = products.order_by('price')
    elif sort_by == 'price_desc':
        products = products.order_by('-price')
    elif sort_by == 'name_asc':
        products = products.order_by('name')
    elif sort_by == 'name_desc':
        products = products.order_by('-name')

    context = {
        'products': products,
        'search_query': search_query,
        'min_price': min_price,
        'max_price': max_price,
        'sort_by': sort_by,
    }
    return render(request, 'products/seller_dashboard.html', context)
# def seller_dashboard(request):
#     """Seller dashboard to manage products."""
#     seller = request.user.seller_profile
#     products = Product.objects.filter(seller=seller)
#     return render(request, 'products/seller_dashboard.html', {'products': products})

@seller_required
def add_product(request):
    seller = request.user.seller_profile
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = seller
            product.save()
            return redirect('products:seller_dashboard')
    else:
        form = ProductForm()
    return render(request, 'products/add_product.html', {'form': form})

@seller_required
def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user.seller_profile)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('products:seller_dashboard')
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/edit_product.html', {'form': form, 'product': product})

@seller_required
def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id, seller=request.user.seller_profile)
    if request.method == 'POST':
        product.delete()
        return redirect('products:seller_dashboard')
    return render(request, 'products/delete_product.html', {'product': product})
