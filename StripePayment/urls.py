from django.contrib import admin
from django.urls import path
from products.views import (
    CreateCheckoutSessionView,
    ItemDetailView,
    PaymentSuccessView,
    PaymentCancelView
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('item/<int:pk>', ItemDetailView.as_view(), name='item-detail'),
    path('success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('cancel/', PaymentCancelView.as_view(), name='payment-cancel'),
    path('buy/<int:pk>', CreateCheckoutSessionView.as_view(), name='create-checkout-session')
]
