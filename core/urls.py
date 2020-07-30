from django.urls import path
from .views import (
    homeView,
    cart,
    checkout,
    updateItem,
    orderProcess
)
app_name = 'store'

urlpatterns = [
    path('', homeView.as_view(),name='home'),
    path('cart/', cart,name='cart'),
    path('checkout/', checkout,name='checkout'),
    path('update-item/', updateItem,name='update-item'),
    path('order-process/', orderProcess,name='order-process'),
]