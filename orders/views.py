from django.shortcuts import render, redirect, get_object_or_404
from .models import Order, OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.db import transaction
import logging

logger = logging.getLogger(__name__)

# Create your views here.

@login_required(login_url='login')
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():  # Use transaction to ensure all operations succeed or none do
                    order = form.save(commit=False)
                    order.total_price = cart.get_total_price()
                    
                    # Check if all products have sufficient stock
                    for item in cart:
                        product = item['product']
                        if product.stock < item['quantity']:
                            messages.error(request, f'Sorry, only {product.stock} units of {product.name} are available.')
                            return render(request, 'orders/order/create.html',
                                     {'cart': cart, 'form': form})
                    
                    order.save()
                    
                    # Create order items and update stock
                    for item in cart:
                        product = item['product']
                        quantity = item['quantity']
                        
                        # Create order item
                        OrderItem.objects.create(
                            order=order,
                            product=product,
                            price=item['price'],
                            quantity=quantity
                        )
                        
                        # Update product stock
                        product.stock -= quantity
                        product.save()
                    
                    # Clear the cart
                    cart.clear()
                    
                    # Send order confirmation email
                    try:
                        subject = f'Buddy Store - Order #{order.id} Confirmation'
                        html_message = render_to_string('orders/order/email/order_confirmation.html', {
                            'order': order,
                            'total_price': order.total_price,
                        })
                        plain_message = f"""
                        Thank you for your order #{order.id}!
                        
                        Total Amount: ₹{order.total_price}
                        
                        We will process your order as soon as possible.
                        
                        Best regards,
                        Buddy Store Team
                        """
                        
                        sent = send_mail(
                            subject=subject,
                            message=plain_message,
                            from_email=settings.EMAIL_HOST_USER,
                            recipient_list=[order.email],
                            html_message=html_message,
                            fail_silently=False,
                        )
                        
                        if sent:
                            logger.info(f"Order confirmation email sent successfully to {order.email}")
                            messages.success(request, 'Order placed successfully! We have sent you a confirmation email.')
                        else:
                            logger.warning(f"Failed to send order confirmation email to {order.email}")
                            messages.warning(request, 'Order placed successfully! However, we could not send you a confirmation email.')
                            
                    except Exception as e:
                        logger.error(f"Error sending order confirmation email: {str(e)}")
                        messages.warning(request, 'Order placed successfully! However, we could not send you a confirmation email.')
                    
                    return render(request, 'orders/order/created.html',
                             {'order': order})
                             
            except Exception as e:
                logger.error(f"Error creating order: {str(e)}")
                messages.error(request, 'There was an error processing your order. Please try again.')
                return render(request, 'orders/order/create.html',
                         {'cart': cart, 'form': form})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html',
                 {'cart': cart, 'form': form})

@login_required(login_url='login')
def order_history(request):
    orders = None
    email = request.GET.get('email')
    
    if email:
        orders = Order.objects.filter(email=email).order_by('-created')
        if not orders:
            messages.warning(request, 'No orders found for this email address.')
    
    return render(request, 'orders/order/history.html', {
        'orders': orders,
        'email': email
    })

@login_required(login_url='login')
def order_detail(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        # Only allow access if the email in the URL matches the order's email
        email = request.GET.get('email')
        if email != order.email:
            raise Http404
        return render(request, 'orders/order/detail.html', {'order': order})
    except Order.DoesNotExist:
        raise Http404

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html',
                 {'order': order})
