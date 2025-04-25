from django.shortcuts import render, get_object_or_404, redirect
from .models import Category, Product, Review
from cart.forms import CartAddProductForm
from .forms import ReviewForm
from django.contrib import messages
from orders.models import Order

# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    
    # Add cart form for each product
    for product in products:
        product.cart_form = CartAddProductForm()
    
    return render(request, 'products/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_add_form = CartAddProductForm()
    reviews = product.reviews.filter(active=True)
    new_review = None

    if request.method == 'POST':
        review_form = ReviewForm(data=request.POST)
        if review_form.is_valid():
            new_review = review_form.save(commit=False)
            new_review.product = product
            new_review.save()
            messages.success(request, 'Your review has been added successfully!')
            return redirect(product.get_absolute_url())
    else:
        review_form = ReviewForm()

    return render(request, 'products/product/detail.html', {
        'product': product,
        'cart_add_form': cart_add_form,
        'reviews': reviews,
        'new_review': new_review,
        'review_form': review_form
    })

def about_us(request):
    return render(request, 'products/about.html')

def home(request):
    categories = Category.objects.all()
    featured_products = Product.objects.filter(featured=True)[:8]
    
    # Handle order history search
    orders = None
    search_email = request.GET.get('email')
    if search_email:
        try:
            orders = Order.objects.filter(email=search_email).order_by('-created')[:5]  # Show last 5 orders
            if not orders.exists():
                messages.info(request, 'No orders found for this email address.')
        except Exception as e:
            messages.error(request, 'Error retrieving orders. Please try again.')
            print(f"Error retrieving orders: {str(e)}")
    
    return render(request, 'products/home.html', {
        'categories': categories,
        'featured_products': featured_products,
        'orders': orders,
        'search_email': search_email,
    })

def pet_guides(request):
    """View function for the pet care guides page"""
    categories = Category.objects.all()
    return render(request, 'products/pet_guides.html', {
        'categories': categories,
    })
