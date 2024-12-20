from django.shortcuts import render, redirect
from .utils import get_cart_data, CartFormAuthenticatedUser, CartForAnonymousUser
from .forms import CustomForm

def cart_view(request):
    cart_info = get_cart_data(request)
    context = {
        'cart_total_quantity': cart_info['cart_total_quantity'],
        'cart_total_price': cart_info['cart_total_price'],
        'order': cart_info['order'],
        'products': cart_info['products'],
    }
    return render(request, 'pages/cart.html', context)

def to_cart(request, product_id, action):
    if not request.user.is_authenticated:
        session_cart = CartForAnonymousUser(request, product_id, action)
    else:
        user_cart = CartFormAuthenticatedUser(request, product_id, action)


    return redirect('cart')



def checkout_view(request):
    cart_info = get_cart_data(request)
    context = {
        'customer_form': CustomForm(),
        # 'shipping_form': ShippingAddressForm(),
        'order': cart_info['order'],
        'products': cart_info['products'],

    }
    return render(request, 'pages/checkout.html', context)


