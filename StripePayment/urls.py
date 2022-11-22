from django.contrib import admin
from django.urls import path, include
from products.views import (
    PaymentSuccessView,
    PaymentCancelView,
    a_create_checkout_session_view,
    a_create_group_checkout_session_view,
)


urlpatterns = [
    # ADMIN VIEWS
    path('admin/', admin.site.urls),

    # CART VIEWS
    path('cart/', include('cart.urls', namespace='cart')),

    # PRODUCTS VIEWS
    path('item/', include('products.urls', namespace='products')),

    # PAYMENT VIEWS
    path('buy/<int:pk>', a_create_checkout_session_view, name='a-create-checkout-session'),
    path('buy/group/', a_create_group_checkout_session_view, name='a-create-group-checkout-session'),
    path('success/', PaymentSuccessView.as_view(), name='payment-success'),
    path('cancel/', PaymentCancelView.as_view(), name='payment-cancel')
]
