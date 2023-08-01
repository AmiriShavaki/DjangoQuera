from django.http import JsonResponse
from .models import Product, Order, OrderItem
from django.shortcuts import get_object_or_404

def checkout(request, order_pk):
    
    order = get_object_or_404(Order, pk=order_pk)

    total_price = 0
    for item in order.orderitem_set.all():
        total_price += item.quantity * item.product.price

    return JsonResponse({"total_price": "{:.2f}".format( total_price )})