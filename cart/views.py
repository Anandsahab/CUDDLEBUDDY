from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from products.models import Product
from .cart import Cart
from .forms import CartAddProductForm
from decimal import Decimal

# Create your views here.

@require_POST
@login_required(login_url='login')
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                quantity=cd['quantity'],
                override_quantity=cd['override'])
    return redirect('cart:cart_detail')

@require_POST
@login_required(login_url='login')
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

@login_required(login_url='login')
def cart_detail(request):
    cart = Cart(request)
    # Get all product IDs from the cart
    product_ids = cart.cart.keys()
    # Get all products from the database
    products = Product.objects.filter(id__in=product_ids)
    cart_items = []
    
    # Create a dictionary of products for easy lookup
    products_dict = {str(p.id): p for p in products}
    
    # Build cart items list
    for product_id, item_data in cart.cart.items():
        product = products_dict.get(product_id)
        if product:
            cart_items.append({
                'product': product,
                'quantity': item_data['quantity'],
                'price': item_data['price'],
                'total_price': Decimal(item_data['price']) * item_data['quantity']
            })
    
    return render(request, 'cart/detail.html', {
        'cart': cart,
        'cart_items': cart_items
    })
