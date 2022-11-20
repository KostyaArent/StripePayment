from decimal import Decimal
from django.conf import settings
from products.models import Item


class Cart(object):

    def __init__(self, request):
        """
        Cart initialize
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, item):
        """
        Add item to cart or update his quantity.
        """
        item_id = str(item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {
                'price': str(item.price)
            }
        self.save()

    def save(self):
        # Update cart session
        self.session[settings.CART_SESSION_ID] = self.cart
        # Mark session like "modified", to make sure it is saved
        self.session.modified = True

    def remove(self, item):
        """
        Remove items from cart.
        """
        item_id = str(item.id)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def __iter__(self):
        """
        Enumeration through items in the cart and getting items from the database.
        """
        items_ids = self.cart.keys()
        # getting item objects and adding them to cart
        items = Item.objects.filter(id__in=items_ids)
        for item in items:
            self.cart[str(item.id)]['item'] = item

        for item in self.cart.values():
            item['price'] = Decimal(item['price'])
            item['display_price'] = item['price']/100
            yield item

    def __len__(self):
        """
        Calculate quantity of all items in cart.
        """
        return len(self.cart.values())

    def get_total_price(self):
        """
        Calculate items total sum in cart.
        """
        return sum(Decimal(item['price']) for item in self.cart.values()) / 100

    def clear(self):
        # delete cart from session
        del self.session[settings.CART_SESSION_ID]
        self.session.modified = True
