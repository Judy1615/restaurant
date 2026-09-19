from .cart import Cart

def cart_count(request):
    if request.user.is_authenticated and not request.user.is_staff:
        return {'cart_count': len(Cart(request))}
    return {'cart_count': 0}