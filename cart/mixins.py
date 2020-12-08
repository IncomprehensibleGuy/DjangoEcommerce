from django.views.generic import View

#from shop.models import Customer, Cart
from .cart import Cart

class CartMixin(View):

    def dispatch(self, request, *args, **kwargs):
        # if request.user.is_authenticated:
        #     customer = Customer.objects.filter(user=request.user).first()
        #     if not customer:
        #         customer = Customer.objects.create(user=request.user)
        #     cart = Cart.objects.filter(owner=customer, in_order=False).first()
        #     if not cart:
        #         cart = Cart.objects.create(owner=customer)
        # else:
        #     cart = Cart.objects.filter(for_anonymous_user=True).first()
        #     if not cart:
        #         cart = Cart.objects.create(for_anonymous_user=True)
        self.cart = Cart(request)
        self.total_price = self.cart.get_total_price()
        self.total_products = self.cart.__len__()
        return super().dispatch(request, *args, **kwargs)
