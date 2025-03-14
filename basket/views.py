from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from store.models import Product
from .basket import Basket


def basket_summary(request):
    basket = Basket(request)
    return render(request, 'basket/basket.html', {'basket': basket})


def basket_add(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        # lấy product theo id trong database
        product = get_object_or_404(Product, id=product_id)
        basket.add(product=product, qty=product_qty)

        basket_qty = basket.__len__()
        response = JsonResponse({'qty': basket_qty})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        basket.delete(product=product_id)

        basket_qty = basket.__len__()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basket_qty, 'subtotal': basket_total})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        basket.update(product=product_id, qty=product_qty)

        basket_qty = basket.__len__()
        basket_subtotal = basket.get_subtotal_price()
        response = JsonResponse({'qty': basket_qty, 'subtotal': basket_subtotal})
        return response


