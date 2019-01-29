from django.shortcuts import render
from django.views.generic import View
from cart.cart import Cart

from .models import OrderItem
from .forms import OrderCreateForm
from .tasks import order_created


class OrderCreateView(View):
    def post(self, request):
        cart = Cart(request)
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # clear the cart
            cart.clear()
            order_created.delay(order.id)
            return render(request,
                          'orders/order/created.html',
                          {'order': order})

    def get(self, request):
        cart = Cart(request)
        form = OrderCreateForm()
        return render(request,
                      'orders/order/create.html',
                      {'cart': cart, 'form': form})
