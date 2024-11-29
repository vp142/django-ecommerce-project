from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Product, Cart, Order
from sellers.models import Seller
from .forms import ProductForm
from django.http import HttpResponseForbidden
from django.http import HttpResponseRedirect
from django.http import Http404
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages
from products.utils import send_email  # Import your send_email function
from django.db.models import Sum
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from .models import Product
# from .serializers import ProductSerializer


stripe.api_key = settings.STRIPE_SECRET_KEY
# @api_view(['GET'])
# def get_products(request):
#     products = Product.objects.all()
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

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
    products = Product.objects.filter(quantity__gt=0)  # Exclude out-of-stock products

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

def add_to_cart(request, product_id):
    """Add a product to the user's cart."""
    product = get_object_or_404(Product, id=product_id)

    # Check stock availability
    if product.quantity <= 0:
        messages.error(request, "This product is out of stock.")
        return redirect('products:all_products')

    # Retrieve or create the cart item for the user and product
    cart, created = Cart.objects.get_or_create(user=request.user, product=product)

    # Check stock before incrementing
    if cart.quantity + 1 > product.quantity:
        messages.error(request, f"Only {product.quantity} items available for {product.name}.")
        return redirect('products:all_products')

    # If it's a new cart item, set the initial quantity to 1
    if created:
        cart.quantity = 1
    else:
        # Increment the quantity if the item is already in the cart
        cart.quantity += 1

    # Save the cart item
    cart.save()

    # Add a success message and redirect
    messages.success(request, f"{product.name} has been added to your cart.")
    return redirect('products:all_products')

@login_required
def view_cart(request):
    """View items in the user's cart."""
    cart_items = Cart.objects.filter(user=request.user)
    
    # Prepare cart data
    cart_data = [
        {
            "id": item.id,
            "product": item.product,
            "quantity": item.quantity,
            "subtotal": item.product.price * item.quantity,
        }
        for item in cart_items
    ]

    # Calculate total price
    total_price = sum(item["subtotal"] for item in cart_data)

    # Pass cart data and total price to the template
    return render(request, 'products/cart.html', {
        'cart_items': cart_data,
        'total_price': total_price,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
    })


@login_required
def remove_from_cart(request, cart_item_id):
    """Remove a product from the cart."""
    try:
        cart_item = Cart.objects.get(id=cart_item_id, user=request.user)
        cart_item.delete()
    except Cart.DoesNotExist:
        raise Http404("The item you're trying to remove doesn't exist.")
    return redirect('products:view_cart')

def create_checkout_session(request):
    """Create a Stripe checkout session."""
    user = request.user
    cart_items = Cart.objects.filter(user=user)

    line_items = []
    for item in cart_items:
        # Check stock availability
        if item.product.quantity < item.quantity:
            return JsonResponse({'error': f"Not enough stock for {item.product.name}."}, status=400)

        # Create Stripe line items
        line_items.append({
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': item.product.name,
                },
                'unit_amount': int(item.product.price * 100),  # Stripe expects amounts in cents
            },
            'quantity': item.quantity,
        })

    # Create a Stripe Checkout session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=line_items,
        mode='payment',
        success_url=request.build_absolute_uri('/products/cart/success/'),
        cancel_url=request.build_absolute_uri('/products/cart/cancel/'),
    )

    return JsonResponse({'id': session.id})

@login_required
def payment_success(request):
    """Handle successful payment and update product stock."""
    user = request.user
    cart_items = Cart.objects.filter(user=request.user)

    # Track current order items
    current_order_items = []

    for item in cart_items:
        # Save each cart item as an order
        order = Order.objects.create(
            user=request.user,
            product=item.product,
            quantity=item.quantity,
            total_price=item.product.price * item.quantity,
        )
        current_order_items.append(order)  # Save the newly created orders for the current session

        # Reduce product quantity
        product = item.product
        product.quantity -= item.quantity
        if product.quantity < 0:  # Prevent negative stock
            product.quantity = 0
        product.save()

    # Clear the user's cart
    cart_items.delete()
    messages.success(request, "Your payment was successful!")

    # Calculate total price for the current order
    total_price = sum(order.product.price * order.quantity for order in current_order_items)

    # Prepare email
    subject = "Order Confirmation"
    message = f"""\
    <html>
    <body>
    <div style="font-family: Arial, sans-serif; max-width: 600px; margin: auto; border: 1px solid #ddd; border-radius: 8px; padding: 20px; background-color: #f9f9f9;">
        <h2 style="text-align: center; color: #007bff;">Order Confirmation</h2>
        <p>Dear {user.first_name},</p>
        <p>Thank you for shopping with us! Here are the details of your order:</p>
        <table style="width: 100%; border-collapse: collapse; margin: 20px 0;">
            <thead>
                <tr style="background-color: #f4f4f9; text-align: left;">
                    <th style="border: 1px solid #ddd; padding: 8px;">Product</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Quantity</th>
                    <th style="border: 1px solid #ddd; padding: 8px;">Price</th>
                </tr>
            </thead>
            <tbody>
    """

    for order in current_order_items:
        message += f"""
                <tr>
                    <td style="border: 1px solid #ddd; padding: 8px;">{order.product.name}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">{order.quantity}</td>
                    <td style="border: 1px solid #ddd; padding: 8px;">${order.product.price:.2f}</td>
                </tr>
        """

    message += f"""
            </tbody>
        </table>
        <p style="font-weight: bold;">Total: ${total_price:.2f}</p>
        <p>We hope to see you again soon!</p>
        <p>Best regards,<br>E-commerce Team</p>
    </div>
    </body>
    </html>
    """

    # Send email
    send_email(subject, message, user.email)

    # Render the success page
    return render(request, 'products/payment_success.html')



def payment_cancel(request):
    """Render a payment canceled page."""
    return render(request, 'products/payment_cancel.html')

@login_required
def user_orders(request):
    """View for regular users to see their orders."""
    orders = Order.objects.filter(user=request.user)
    return render(request, 'products/user_orders.html', {'orders': orders})

@login_required
@seller_required
def seller_orders(request):
    """View to display orders for the seller's products grouped by product."""
    seller = request.user.seller_profile
    # Aggregate total quantity sold for each product sold by the seller
    orders = Order.objects.filter(product__seller=seller).values(
        'product__name', 'product__price'
    ).annotate(
        total_quantity=Sum('quantity'),
        total_revenue=Sum('total_price')
    )

    return render(request, 'products/seller_orders.html', {
        'orders': orders,
    })