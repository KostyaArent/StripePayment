import stripe

from asgiref.sync import sync_to_async

from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import (
    TemplateView, DetailView,
    ListView
)

from cart.cart import Cart
from .models import Item


stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemListView(ListView):
    paginate_by = 6
    model = Item
    context_object_name = "item_list"
    template_name = "item_list.html"

    def get_context_data(self, **kwargs):
        context = super(ItemListView, self).get_context_data(**kwargs)
        context.update({
            "cart": Cart(self.request),
        })
        return context


class ItemDetailView(DetailView):
    template_name = "item.html"
    model = Item

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLISHABLE_KEY,
        })
        return context


class PaymentSuccessView(TemplateView):
    template_name = "payment/success.html"


class PaymentCancelView(TemplateView):
    template_name = "payment/cancel.html"


async def a_create_checkout_session_view(request, pk):
    method = request.method
    if method != "GET":
        return JsonResponse({
            'detail': "method {} not found.".format(method)}, status=405)

    success_url = request.build_absolute_uri(reverse('payment-success', ))
    cancel_url = request.build_absolute_uri(reverse('payment-cancel', ))
    item = await Item.objects.filter(pk=pk).afirst()
    if not item:
        return JsonResponse({
            'detail': "item with id {} not found.".format(pk)}, status=404)
    line_items = [
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': item.name,
                    },
                    'unit_amount': item.price,
                },
                'quantity': 1,
            },
        ]
    try:
        checkout_session = await sync_to_async(stripe.checkout.Session.create)(
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url
        )
    except Exception as e:
        return str(e)

    return JsonResponse({
        'sessionId': checkout_session.get('id', None)}, status=200)


async def a_create_group_checkout_session_view(request):
    method = request.method
    if method != "GET":
        return JsonResponse({
            'detail': "method {} not found.".format(method)}, status=405)
    success_url = request.build_absolute_uri(reverse('payment-success', ))
    cancel_url = request.build_absolute_uri(reverse('payment-cancel', ))
    cart = await sync_to_async(Cart)(request)
    # print(list(cart.values()))
    line_items = [{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': item['item'],
                        },
                        'unit_amount': str(item['price']),
                    },
                    'quantity': 1,
                } async for item in cart]
    try:
        checkout_session = await sync_to_async(stripe.checkout.Session.create)(
            line_items=line_items,
            mode='payment',
            success_url=success_url,
            cancel_url=cancel_url
        )
    except Exception as e:
        return str(e)

    return JsonResponse({
        'sessionId': checkout_session.get('id', None)}, status=200)
