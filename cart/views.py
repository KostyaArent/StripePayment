from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404, render
from django.views.decorators.http import require_POST
from products.models import Item
from .cart import Cart


@require_POST
def cart_add(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, pk=item_id)
    cart.add(item=item)
    return JsonResponse({
            'status': 200
        })


def cart_remove(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(Item, id=item_id)
    cart.remove(item)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})