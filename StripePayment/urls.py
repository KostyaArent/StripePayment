from django.contrib import admin
from django.urls import path, include
from products.views import (
    ItemDetailView,
    PaymentSuccessView,
    PaymentCancelView,
    a_create_checkout_session_view,
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('cart/', include('cart.urls', namespace='cart')),
    path('item/<int:pk>', ItemDetailView.as_view(), name='item-detail'),
    path('buy/<int:pk>', a_create_checkout_session_view, name='a-create-checkout-session'),
    path('success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('cancel/', PaymentCancelView.as_view(), name='payment-cancel')
]
