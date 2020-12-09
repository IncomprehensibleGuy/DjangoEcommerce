from .cart import Cart


def cart(request):
    cart = Cart(request)
    return {
        'cart': cart,
        'total_price': cart.get_total_price(),
        'total_products': cart.__len__()
    }
