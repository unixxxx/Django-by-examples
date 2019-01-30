from django.shortcuts import render, redirect
from django.views.generic import View
from django.urls import reverse
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
            request.session['order_id'] = order.id
            return redirect(reverse('payment:process'))

    def get(self, request):
        cart = Cart(request)
        form = OrderCreateForm()
        return render(request,
                      'orders/order/create.html',
                      {'cart': cart, 'form': form})
