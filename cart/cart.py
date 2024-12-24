from store.models import Product
from user.models import Profile


class Cart:
    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')

        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def get_total(self):
        # Get store IDS
        products_id = self.cart.keys()
        # lookup those keys in our store database model
        products = Product.objects.filter(id__in=products_id)
        # Get quantities
        quantities = self.cart
        # Start Counting at 0
        total = 0

        #    {'2': 3}
        for key, value in quantities.items():

            # Convert key string into int so we can do math
            key = int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += (product.sale_price * value)
                    else:
                        total += (product.price * value)
        return total

    def db_add(self, product, quantity):
        product_id = str(product)
        product_qty = str(quantity)

        # logic
        if product_id in self.cart:
            pass

        else:
            # self.cart[product_id] = {'name': str(product.name), 'price': str(product.price), }
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            # convert {'3':1 , '2':4} to {"3":1 , "2":4}

            carty = str(self.cart).replace("\'", "\"")

            # Save carty to profile Model
            current_user.update(old_cart=str(carty))

    def add(self, product, quantity):
        product_id = str(product.id)
        product_qty = str(quantity)

        if product_id in self.cart:
            pass

        else:
            # self.cart[product_id] = {'name': str(product.name), 'price': str(product.price), }
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace('\'', '\"')

            current_user.update(old_cart=carty)

    def __len__(self):
        return len(self.cart)

    def get_quantity(self):
        return self.cart

    def get_products(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products

    def update(self, product, quantity):
        product_id = str(product)
        product_qty = int(quantity)

        # {'2': 3, '3': 5}
        # get cart
        newCart = self.cart
        # update dictionary/cart
        newCart[product_id] = product_qty

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace('\'', '\"')

            current_user.update(old_cart=carty)

        return self.cart

    def delete(self, product):
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

        if self.request.user.is_authenticated:
            current_user = Profile.objects.filter(user__id=self.request.user.id)
            carty = str(self.cart).replace('\'', '\"')

            current_user.update(old_cart=carty)
