import json

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from StripePayment import settings
from products.models import Item
from .cart import Cart


@require_POST
def cart_add(request):
    body = json.loads(request.body)
    item_id = body.get('item_id', None)
    if not item_id.isnumeric():
        return JsonResponse({'message': f'item with id {item_id} is not numeric'}, status=415)
    cart = Cart(request)
    if item_id in tuple(cart.cart.keys()):
        return JsonResponse({'message': f'item with id {item_id} already in the cart'}, status=409)
    item = get_object_or_404(Item, pk=item_id)
    cart.add(item=item)
    return JsonResponse({'status': 200}, status=200)


@require_POST
def cart_remove(request):
    body = json.loads(request.body)
    item_id = body.get('item_id', None)
    if not item_id.isnumeric():
        return JsonResponse({'message': f'item with id {item_id} is not numeric'}, status=415)
    cart = Cart(request)
    if item_id not in tuple(cart.cart.keys()):
        return JsonResponse({'message': f'item with id {item_id} not in the cart'}, status=409)
    item = get_object_or_404(Item, id=item_id)
    cart.remove(item)
    return JsonResponse({'status': 200}, status=200)


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {
        'cart': cart,
        "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLISHABLE_KEY
    })


@require_POST
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return JsonResponse({}, status=200)
