from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import transaction
from decimal import Decimal
from django.utils.crypto import get_random_string
from datetime import date, timedelta
from .models import Product, Category, Brand, Order, OrderItem, OrderStatus
from .forms import ProductFilterForm, CartAddProductForm, CheckoutForm
from .cart import Cart
from .utils.logging import log_order_processing, OrderError, order_logger
from .utils.order_processing import (
    validate_cart,
    create_order,
    create_order_items,
    process_payment
)

def validate_order_status(status):
    valid_statuses = ['pending', 'processing', 'confirmed', 'cancelled', 'shipped', 'delivered', 'refunded']
    if status not in valid_statuses:
        raise ValidationError(f"Invalid status: {status}")
    return status

def product_list(request):
    products = Product.objects.all()
    form = ProductFilterForm(request.GET)
    
    if form.is_valid():
        # Search filter
        search = form.cleaned_data.get('search')
        if search:
            products = products.filter(
                Q(name__icontains=search) |
                Q(description__icontains=search) |
                Q(category__name__icontains=search) |
                Q(brand__name__icontains=search)
            )
        
        # Category filter
        category = form.cleaned_data.get('category')
        if category:
            products = products.filter(category=category)
        
        # Brand filter
        brand = form.cleaned_data.get('brand')
        if brand:
            products = products.filter(brand=brand)
        
        # Price range filter
        price_range = form.cleaned_data.get('price_range')
        if price_range:
            if price_range == '0-50':
                products = products.filter(price__lt=50)
            elif price_range == '50-100':
                products = products.filter(price__gte=50, price__lt=100)
            elif price_range == '100-200':
                products = products.filter(price__gte=100, price__lt=200)
            elif price_range == '200-500':
                products = products.filter(price__gte=200, price__lt=500)
            elif price_range == '500+':
                products = products.filter(price__gte=500)
        
        # Featured filter
        featured_only = form.cleaned_data.get('featured_only')
        if featured_only:
            products = products.filter(featured=True)
        
        # Available filter
        available_only = form.cleaned_data.get('available_only')
        if available_only:
            products = products.filter(available=True, stock__gt=0)
        
        # Sort filter
        sort_by = form.cleaned_data.get('sort_by')
        if sort_by:
            products = products.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(products, 9)  # Show 9 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'products': page_obj,
        'form': form,
        'total_products': products.count(),
    }
    
    return render(request, 'shop/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)
    related_products = Product.objects.filter(
        category=product.category,
        available=True
    ).exclude(id=product.id)[:4]
    
    cart_product_form = CartAddProductForm()
    
    context = {
        'product': product,
        'related_products': related_products,
        'cart_product_form': cart_product_form,
    }
    
    return render(request, 'shop/product_detail.html', context)

def category_products(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category, available=True)
    
    # Apply pagination
    paginator = Paginator(products, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'products': page_obj,
    }
    
    return render(request, 'shop/category_products.html', context)

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product,
                quantity=cd['quantity'],
                override_quantity=cd['override'])
    return redirect('shop:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('shop:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={
            'quantity': item['quantity'],
            'override': True})
    return render(request, 'shop/cart/detail.html', {'cart': cart})

@login_required
@log_order_processing
def checkout(request):
    cart = Cart(request)
    
    # Check if cart is empty
    if len(cart) == 0:
        messages.error(request, "Your cart is empty!")
        return redirect('shop:product_list')
    
    # Lock prevention - store cart version in session
    cart_version = request.session.get('cart_version', 0)
        
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Verify cart hasn't changed
            if cart_version != request.session.get('cart_version', 0):
                messages.error(request, "Your cart has been modified. Please review your order and try again.")
                return redirect('shop:cart_detail')
            
            try:
                with transaction.atomic():
                    # Step 1: Validate cart and get locked products
                    products_dict = validate_cart(cart, user_id=request.user.id)
                    
                    # Step 2: Create the order
                    order = create_order(form, cart, request.user, products_dict)

                    # Check product availability and stock with proper locking
                    unavailable_products = []
                    products_to_update = []
                    
                    # Lock the products for update
                    product_ids = [item['product'].id for item in cart]
                    products = Product.objects.select_for_update().filter(id__in=product_ids)
                    products_dict = {p.id: p for p in products}
                    
                    for item in cart:
                        product_id = item['product'].id
                        product = products_dict.get(product_id)
                        
                        if not product:
                            unavailable_products.append(f"{item['product'].name} is no longer available")
                            continue
                            
                        if not product.available:
                            unavailable_products.append(f"{product.name} is no longer available for purchase")
                        elif product.stock < item['quantity']:
                            unavailable_products.append(
                                f"{product.name} has insufficient stock (requested: {item['quantity']}, "
                                f"available: {product.stock})"
                            )
                        else:
                            # Store product and quantity for later update
                            products_to_update.append((product, item['quantity']))
                    
                    if unavailable_products:
                        transaction.set_rollback(True)
                        messages.error(request, "Unable to complete your order due to the following issues:")
                        for msg in unavailable_products:
                            messages.error(request, msg)
                        return redirect('shop:cart_detail')

                    # Create order
                    order = form.save(commit=False)
                    order.user = request.user
                    order.status = 'pending'
                    order.payment_status = 'pending'
                    
                    # Set estimated delivery
                    today = date.today()
                    if order.shipping_method == 'express':
                        order.estimated_delivery = today + timedelta(days=3)
                    elif order.shipping_method == 'standard':
                        order.estimated_delivery = today + timedelta(days=7)
                    elif order.shipping_method == 'pickup':
                        order.estimated_delivery = today + timedelta(days=1)

                    # Calculate totals
                    subtotal = Decimal(str(cart.get_total_price()))
                    shipping_cost = Decimal('0.00')
                    
                    if order.shipping_method == 'standard':
                        shipping_cost = Decimal('5.00')
                    elif order.shipping_method == 'express':
                        shipping_cost = Decimal('15.00')
                    
                    tax = (subtotal + shipping_cost) * Decimal('0.10')
                    
                    order.subtotal = subtotal
                    order.shipping_cost = shipping_cost
                    order.tax = tax
                    order.total_amount = subtotal + shipping_cost + tax

                    # Generate tracking number
                    tracking_number = get_random_string(10).upper()
                    order.tracking_number = tracking_number
                    order.save()

                    # Step 3: Create order items and update stock
                    create_order_items(order, cart, products_dict)
                    
                    # Step 4: Process payment and update status
                    process_payment(order)
                    
                    # Create initial success status
                    OrderStatus.objects.create(
                        order=order,
                        status='pending',
                        note='Order placed successfully',
                        created_by=request.user
                    )

                    # Process payment
                    if order.payment_method == 'cash_on_delivery':
                        new_status = 'confirmed'
                        payment_status = 'pending'
                        status_note = 'Order confirmed - Cash on Delivery'
                    else:
                        new_status = 'processing'
                        payment_status = 'completed'
                        status_note = 'Payment processed successfully'

                    # Update order status
                    validate_order_status(new_status)
                    order.status = new_status
                    order.payment_status = payment_status
                    order.save()

                    # Create payment status update
                    OrderStatus.objects.create(
                        order=order,
                        status=new_status,
                        note=status_note,
                        created_by=request.user
                    )

                    # Send confirmation email
                    try:
                        from .utils import send_order_confirmation_email
                        email_sent = send_order_confirmation_email(request, order)
                        if email_sent:
                            messages.success(
                                request,
                                f"Order #{order.id} placed successfully! "
                                f"Current Status: {order.get_status_display()}. "
                                f"A confirmation email has been sent to {order.email}"
                            )
                        else:
                            messages.warning(
                                request,
                                f"Order #{order.id} placed successfully. "
                                f"Please save your tracking number: {order.tracking_number}. "
                                "The confirmation email could not be sent."
                            )
                    except Exception:
                        messages.warning(
                            request,
                            f"Order #{order.id} placed successfully. "
                            f"Please save your tracking number: {order.tracking_number}. "
                            "The confirmation email could not be sent."
                        )

                    # Store order details and clear cart
                    request.session['recent_order_id'] = order.id
                    request.session['order_tracking_number'] = order.tracking_number
                    cart.clear()
                    
                    return redirect('shop:order_confirmation', order_id=order.id)

            except OrderError as e:
                # Handle specific order processing errors
                error_messages = {
                    'EMPTY_CART': "Your cart appears to be empty. Please add items and try again.",
                    'PRODUCT_UNAVAILABLE': "Some products in your cart are no longer available.",
                    'PAYMENT_ERROR': "There was an error processing your payment. Please try again.",
                    'STOCK_ERROR': "Some items in your cart are no longer in stock.",
                    'LOCK_ERROR': "The system is currently busy processing other orders. Please try again in a moment.",
                }
                
                error_msg = error_messages.get(e.code, str(e))
                messages.error(request, error_msg)
                
                # Log the error with additional context
                order_logger.error(
                    f"Order processing error: {error_msg}",
                    extra={
                        'error_code': e.code,
                        'user_id': request.user.id,
                        'cart_items': len(cart),
                        'error_details': e.details if hasattr(e, 'details') else None
                    }
                )
                
                if hasattr(e, 'details') and e.details:
                    for detail in e.details:
                        messages.error(request, detail)
                
                if e.code == 'LOCK_ERROR':
                    # For lock errors, stay on checkout page and show retry message
                    messages.info(request, "You can try again in a few seconds.")
                    return redirect('shop:checkout')
                else:
                    # For other errors, redirect based on the error type
                    return redirect('shop:cart_detail' if e.code in ['EMPTY_CART', 'PRODUCT_UNAVAILABLE', 'STOCK_ERROR'] else 'shop:checkout')
                
            except ValidationError as e:
                messages.error(request, f"Please check your information: {str(e)}")
                return redirect('shop:checkout')
                
            except transaction.TransactionManagementError:
                messages.error(
                    request,
                    "There was a problem processing your order due to a system issue. "
                    "Please try again in a few moments."
                )
                return redirect('shop:checkout')
                
            except Exception as e:
                # Log unexpected errors with full context
                order_logger.error(
                    f"Critical error during checkout for user {request.user.id}",
                    extra={
                        'user_id': request.user.id,
                        'error': str(e),
                        'cart_items': len(cart),
                        'total_amount': cart.get_total_price()
                    }
                )
                
                messages.error(
                    request,
                    "We encountered a technical issue while processing your order. "
                    "Our team has been notified and is working to resolve it. "
                    "Please try again in a few minutes or contact our support if the issue persists."
                )
    else:
        # Pre-fill form with user data if available
        initial_data = {}
        if request.user.first_name:
            initial_data['first_name'] = request.user.first_name
        if request.user.last_name:
            initial_data['last_name'] = request.user.last_name
        if request.user.email:
            initial_data['email'] = request.user.email
        form = CheckoutForm(initial=initial_data)
    
    return render(request, 'shop/checkout.html', {
        'cart': cart,
        'form': form
    })

@login_required
def order_confirmation(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Validate order has items
    if not order.items.exists():
        messages.warning(request, "This order has no items.")
    
    # Validate order status
    try:
        validate_order_status(order.status)
    except ValidationError as e:
        messages.error(request, str(e))
        order.status = 'pending'  # Set to default status
        order.save()
    
    return render(request, 'shop/order_confirmation.html', {'order': order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'shop/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    status_updates = order.status_updates.all().order_by('-timestamp')
    return render(request, 'shop/order_detail.html', {
        'order': order,
        'status_updates': status_updates
    })

def track_order(request):
    # Status weights for progress calculation
    status_weights = {
        'pending': 0,
        'processing': 20,
        'confirmed': 40,
        'shipped': 60,
        'out_for_delivery': 80,
        'delivered': 100,
        'cancelled': -1,
        'refunded': -1
    }

    # Get tracking number from either POST or GET
    tracking_number = request.POST.get('tracking_number') or request.GET.get('order_number')
    
    if tracking_number:
        try:
            # Try to find order by tracking number or ID
            try:
                order = Order.objects.get(tracking_number=tracking_number)
            except Order.DoesNotExist:
                try:
                    order = Order.objects.get(id=tracking_number)
                except (Order.DoesNotExist, ValueError):
                    messages.error(request, 'Order not found. Please check your tracking number.')
                    return render(request, 'shop/track_order_form.html')

            # Calculate progress percentage
            progress_percentage = status_weights.get(order.status, 0)
            
            # If order is cancelled or refunded, show appropriate message
            if order.status in ['cancelled', 'refunded']:
                messages.warning(request, f'This order has been {order.status}.')
                progress_percentage = 0

            context = {
                'order': order,
                'progress_percentage': progress_percentage,
                'status_updates': order.status_updates.all().order_by('-timestamp'),
            }
            
            return render(request, 'shop/track_order.html', context)
            
        except Exception:
            messages.error(request, 'An error occurred while tracking your order. Please try again.')
            return render(request, 'shop/track_order_form.html')

    # If no tracking number provided, show the tracking form
    return render(request, 'shop/track_order_form.html')