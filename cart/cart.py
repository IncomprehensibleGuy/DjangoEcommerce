from base.settings import CART_SESSION_ID
from shop.models import Product


class Cart:

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart
        self.total_products = 0

    def __iter__(self):
        ''' Перебор элементов в корзине и получение продуктов из базы данных. '''
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        for product in products:
            self.cart[str(product.id)]['product'] = product

        for item in self.cart.values():
            item['price'] = int(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        ''' Подсчет всех товаров в корзине. '''
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        ''' Подсчет стоимости товаров в корзине. '''
        return sum(int(item['price']) * item['quantity'] for item in self.cart.values())

    def save(self):
        ''' Updating session cart '''
        self.session[CART_SESSION_ID] = self.cart
        self.session.modified = True

    def clear(self):
        ''' Delete cart from session '''
        del self.session[CART_SESSION_ID]
        self.session.modified = True

    def recalculate(self):
        ''' Update values of cart's total products and cart's total price. '''
        self.total_price = self.get_total_price()
        self.total_products = self.__len__()
        self.save()

    def add_product(self, product, quantity=1):
        product_id = str(product.id)
        if product_id not in self.cart:
            total_price = product.price * quantity
            self.cart[product_id] = {
                'price': str(product.price),
                'quantity': quantity,
                'total_price': str(total_price),
                'slug': product.slug
            }
        else:
            self.cart[product_id]['quantity'] += quantity
        self.recalculate()

    def change_product_quantity(self, product, quantity):
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.recalculate()

    def remove_product(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.recalculate()
