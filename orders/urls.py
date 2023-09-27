from django.urls import path, include
from orders.views import AddOrderView

urlpatterns = [
    path('add/', AddOrderView.as_view(), name='add_order'),
]
