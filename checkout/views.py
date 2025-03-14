import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from account.models import Address
from basket.basket import Basket
from orders.models import Order, OrderItem
from .models import DeliveryOptions
from paypalcheckoutsdk.orders import OrdersGetRequest
from .paypal import PayPalClient

from django.shortcuts import redirect


@login_required
def delivery_choices(request):
    deliveryOptions = DeliveryOptions.objects.filter(is_active=True)
    return render(request, "checkout/delivery_choices.html", {"deliveryoptions": deliveryOptions})


@login_required
def basket_update_delivery(request):
    basket = Basket(request)
    if request.POST.get("action") == "post":
        delivery_id = int(request.POST.get("delivery_id"))
        # Lấy phương thức vận chuyển theo id
        delivery = DeliveryOptions.objects.get(id=delivery_id)
        updated_total_price = basket.basket_update_delivery(delivery.delivery_price)

        session = request.session
        # nếu không tồn tại delivery thì khởi tạo, còn tồn tại thì update trong session
        if "delivery" not in request.session:
            session["delivery"] = {
                "delivery_id": delivery.id,
            }
        else:
            session["delivery"]["delivery_id"] = delivery.id
            session.modified = True

        response = JsonResponse({"total": updated_total_price, "delivery_price": delivery.delivery_price})
        return response


@login_required
def delivery_address(request):
    session = request.session
    if "delivery" not in request.session:
        messages.success(request, "Vui lòng chọn phương thức vận chuyển")
        # chưa chọn thì quay lại trang gửi request thông báo cho người dùng
        return HttpResponseRedirect(request.META["HTTP_REFERER"])

    addresses = Address.objects.filter(customer=request.user).order_by("-default")

    # nếu không tồn tại địa chỉ thì tạo mới, ngược lại thì update trong session
    if "address" not in request.session:
        session["address"] = {"address_id": str(addresses[0].id)}
    else:
        session["address"]["address_id"] = str(addresses[0].id)
        session.modified = True

    return render(request, "checkout/delivery_address.html", {"addresses": addresses})

# @login_required
# def delivery_address(request):
#     session = request.session

#     if "delivery" not in request.session:
#         messages.success(request, "Vui lòng chọn phương thức vận chuyển")
#         return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))

#     # Lấy danh sách địa chỉ của user
#     addresses = Address.objects.filter(customer=request.user).order_by("-default")

#     if not addresses.exists():  # Kiểm tra nếu không có địa chỉ nào
#         messages.warning(request, "Bạn chưa có địa chỉ nào, vui lòng thêm mới!")
#         from django.urls import reverse

#         return redirect(reverse("add_address"))


#     # Nếu có địa chỉ, kiểm tra session và cập nhật
#     if "address" not in session:
#         session["address"] = {"address_id": str(addresses.first().id)}
#     else:
#         session["address"]["address_id"] = str(addresses.first().id)
#         session.modified = True

#     return render(request, "checkout/delivery_address.html", {"addresses": addresses})



####
# Thanh toán bằng PayPal
####


@login_required
def payment_complete(request):
    PPClient = PayPalClient()

    body = json.loads(request.body)
    data = body["orderID"]
    user_id = request.user.id

    requestOrder = OrdersGetRequest(data)
    response = PPClient.client.execute(requestOrder)

    basket = Basket(request)
    order = Order.objects.create(
        user_id=user_id,
        full_name=response.result.purchase_units[0].shipping.name.full_name,
        email=response.result.payer.email_address,
        address1=response.result.purchase_units[0].shipping.address.address_line_1,
        address2=response.result.purchase_units[0].shipping.address.admin_area_2,
        postal_code=response.result.purchase_units[0].shipping.address.postal_code,
        country_code=response.result.purchase_units[0].shipping.address.country_code,
        total_paid=response.result.purchase_units[0].amount.value,
        order_key=response.result.id,
        payment_option="paypal",
        billing_status=True,
    )
    order_id = order.pk
    for item in basket:
        OrderItem.objects.create(order_id=order_id, product=item["product"], price=item["price"], quantity=item["qty"])
    return JsonResponse("Payment completed!", safe=False)


@login_required
def payment_successful(request):
    basket = Basket(request)
    basket.clear()
    return render(request, "checkout/payment_successful.html", {})
