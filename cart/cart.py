from menu.models import MenuItem

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, item_id, quantity=1):
        item_id = str(item_id)
        if item_id in self.cart:
            self.cart[item_id] += quantity
        else:
            self.cart[item_id] = quantity
        self.save()

    def decrease(self, item_id):
        item_id = str(item_id)
        if item_id in self.cart:
            self.cart[item_id] -= 1
            if self.cart[item_id] <= 0:
                del self.cart[item_id]
        self.save()

    def remove(self, item_id):
        item_id = str(item_id)
        if item_id in self.cart:
            del self.cart[item_id]
        self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        self.session['cart'] = {}
        self.save()

    def __iter__(self):
        item_ids = self.cart.keys()
        items = MenuItem.objects.filter(pk__in=item_ids)
        for item in items:
            data = self.cart[str(item.pk)]
            yield {
                'item': item,
                'quantity': data,
                'subtotal': item.price * data
            }

    def get_total(self):
        return sum(item.price * qty for item, qty in
                   ((MenuItem.objects.get(pk=int(pk)), qty) for pk, qty in self.cart.items()))

    def __len__(self):
        return sum(self.cart.values())