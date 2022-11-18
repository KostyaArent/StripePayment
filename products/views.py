import stripe
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import TemplateView, DetailView

from .models import Item


stripe.api_key = settings.STRIPE_SECRET_KEY


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


class CreateCheckoutSessionView(View):
    def get(self, request, *args, **kwargs):
        success_url = request.build_absolute_uri(reverse('payment-success', ))
        cancel_url = request.build_absolute_uri(reverse('payment-cancel', ))
        item_id = self.kwargs.get("pk")
        item = get_object_or_404(Item, pk=item_id)
        try:
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        # Provide the exact Price ID (for example, pr_1234) of the product you want to sell
                        'price_data': {
                          # The currency parameter determines which
                          # payment methods are used in the Checkout Session.
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
            'sessionId': checkout_session.get('id')
        })
