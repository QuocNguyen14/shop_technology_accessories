from decimal import Decimal

from checkout.models import DeliveryOptions
from django.conf import settings
from store.models import Product


class Basket:
    def __init__(self, request):
        self.session = request.session
        # Lấy giỏ hàng
        basket = self.session.get(settings.BASKET_SESSION_ID)
        # nếu không tồn tại giỏ hàng thì khởi tạo basket = {}
        if settings.BASKET_SESSION_ID not in request.session:
            basket = self.session[settings.BASKET_SESSION_ID] = {}
        self.basket = basket

    # Sử dụng lấy danh sách product hiển thị trong file basket.html
    def __iter__(self):
        product_ids = self.basket.keys()
        products = Product.objects.filter(id__in=product_ids)
        basket = self.basket.copy()

        for product in products:
            # gán product vào basket tương ứng thông qua khóa là str(product.id).
            basket[str(product.id)]["product"] = product

        for item in basket.values():
            item["price"] = Decimal(item["price"])
            item["total_price"] = item["price"] * item["qty"]
            yield item

    # Lấy tổng số lượng các mặt hàng để hiển thị số trên giỏ hàng
    def __len__(self):
        return sum(item["qty"] for item in self.basket.values())

    def add(self, product, qty):
        product_id = str(product.id)

        if product_id in self.basket:
            self.basket[product_id]["qty"] = qty
        else:
            self.basket[product_id] = {"price": str(product.regular_price - product.discount_price), "qty": qty}

        self.save()

    def update(self, product, qty):
        product_id = str(product)
        if product_id in self.basket:
            self.basket[product_id]["qty"] = qty
        self.save()

    # Sử dụng tính tổng tiền sản phẩm của giỏ hàng
    def get_subtotal_price(self):
        return sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())

    # Sử dụng để xem phí vận chuyển ở trang delivery_choices.html, delivery_address.html
    def get_delivery_price(self):
        newPrice = 0.00
        # Kiểm tra nếu session có delivery thì lấy giá tiền vận chuyển
        if "delivery" in self.session:
            newPrice = DeliveryOptions.objects.get(id=self.session["delivery"]["delivery_id"]).delivery_price

        return newPrice

    def get_total_price(self):
        newPrice = 0.00
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())

        if "delivery" in self.session:
            newPrice = DeliveryOptions.objects.get(id=self.session["delivery"]["delivery_id"]).delivery_price

        total = subtotal + Decimal(newPrice)
        return total

    def basket_update_delivery(self, deliveryPrice=0):
        subtotal = sum(Decimal(item["price"]) * item["qty"] for item in self.basket.values())
        total = subtotal + Decimal(deliveryPrice)
        return total

    def delete(self, product):
        product_id = str(product)

        if product_id in self.basket:
            del self.basket[product_id]
            self.save()

    def clear(self):
        # Remove basket from session
        del self.session[settings.BASKET_SESSION_ID]
        self.save()

    def save(self):
        self.session.modified = True
