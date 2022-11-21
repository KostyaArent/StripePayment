from django.urls import path
from products.views import (
    ItemDetailView,
    ItemListView
)

app_name = 'products'

urlpatterns = [
    path('', ItemListView.as_view(), name='item-list'),
    path('<int:pk>', ItemDetailView.as_view(), name='item-detail')
]
