import stripe

from asgiref.sync import sync_to_async

from django.conf import settings
from django.http import JsonResponse
from django.urls import reverse
from django.views.generic import TemplateView, DetailView

from .models import Item


stripe.api_key = settings.STRIPE_SECRET_KEY


class ItemDetailView(DetailView):
    template_name = "item.html"
    model = Item

    def get_context_data(self, **kwargs):
        context = super(ItemDetailView, self).get_context_data(**kwargs)
        cart_item_form = CartAddItemForm()
        context.update({
            "STRIPE_PUBLIC_KEY": settings.STRIPE_PUBLISHABLE_KEY,
            "cart_product_form": cart_item_form
        })
        return context


class PaymentSuccessView(TemplateView):
    template_name = "payment/success.html"


class PaymentCancelView(TemplateView):
    template_name = "payment/cancel.html"


async def a_create_checkout_session_view(request, pk):
    method = request.method
    if method == "GET":
        success_url = request.build_absolute_uri(reverse('payment-success', ))
        cancel_url = request.build_absolute_uri(reverse('payment-cancel', ))
        item = await Item.objects.filter(pk=pk).afirst()
        if not item:
            return JsonResponse({
                'status': 404,
                'detail': "item with id {} not found.".format(pk)
            })
        try:
            checkout_session = await sync_to_async(stripe.checkout.Session.create)(
                line_items=[
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
                ],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url
            )
        except Exception as e:
            return str(e)

        return JsonResponse({
            'status': 200,
            'sessionId': checkout_session.get('id', None)
        })
    else:
        return JsonResponse({
            'status': 405,
            'detail': "Method {} is not allowed.".format(method)
        })
