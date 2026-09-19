from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from menu.models import MenuItem
from .cart import Cart

@login_required
def cart_add(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(MenuItem, pk=item_id)
    cart.add(item.id)
    return redirect(request.META.get('HTTP_REFERER', 'cart:cart_detail'))

@login_required
def cart_decrease(request, item_id):
    cart = Cart(request)
    cart.decrease(item_id)
    return redirect('cart:cart_detail')

@login_required
def cart_remove(request, item_id):
    cart = Cart(request)
    cart.remove(item_id)
    return redirect('cart:cart_detail')

@login_required
def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

from django.contrib import messages

from .models import Order, OrderItem

@login_required
def checkout(request):
    cart = Cart(request)
    if len(cart) == 0:
        return redirect('menu:menu_list')

    if request.method == 'POST':
        address = request.POST.get('address')
        payment_method = request.POST.get('payment_method')

        order = Order.objects.create(
            customer=request.user,
            address=address,
            payment_method=payment_method,
            total=cart.get_total()
        )
        for row in cart:
            OrderItem.objects.create(
                order=order,
                item=row['item'],
                item_name=row['item'].name,
                price=row['item'].price,
                quantity=row['quantity']
            )

        cart.clear()
        messages.success(request, "تم استلام طلبك بنجاح! 🎉")
        return redirect('cart:order_history')

    return render(request, 'cart/checkout.html', {'cart': cart})


@login_required
def order_history(request):
    orders = Order.objects.filter(customer=request.user).order_by('-created_at')
    return render(request, 'cart/order_history.html', {'orders': orders})

# Create your views here.
