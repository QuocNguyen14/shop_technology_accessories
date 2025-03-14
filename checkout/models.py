from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings  # Import settings để lấy AUTH_USER_MODEL
from django.contrib.auth.models import User


class DeliveryOptions(models.Model):
    DELIVERY_CHOICES = [
        ("standard-shipping", "Standard Shipping"),
        ("express-shipping", "Express Shipping"),
        ("same-day-delivery", "Same-day delivery"),
        ("in-store-pickup", "In-store pickup"),
        ("digital-delivery", "Digital delivery"),
    ]

    delivery_name = models.CharField(
        verbose_name=_("Tên vận chuyển:"),
        help_text=_("Bắt buộc"),
        max_length=255,
    )
    delivery_price = models.DecimalField(
        verbose_name=_("Giá"),
        help_text=_("Tối đa 999.999đ"),
        error_messages={
            "name": {
                "max_length": _("Giá phải nằm trong khoảng từ 0 đến 999.999đ"),
            },
        },
        max_digits=8,
        decimal_places=0,
    )
    delivery_method = models.CharField(
        choices=DELIVERY_CHOICES,
        verbose_name=_("Phương thức vận chuyển"),
        help_text=_("Bắt buộc"),
        max_length=255,
    )
    delivery_time = models.CharField(
        verbose_name=_("Thời gian vận chuyển"),
        help_text=_("Bắt buộc"),
        max_length=255,
    )
    order = models.IntegerField(verbose_name=_("Thứ tự ưu tiên:"), help_text=_("Bắt buộc"), default=0)
    is_active = models.BooleanField(verbose_name=_("Trạng thái hoạt động"), default=True)

    class Meta:
        verbose_name = _("Delivery Option")
        verbose_name_plural = _("Delivery Options")

    def __str__(self):
        return self.delivery_name


class PaymentSelections(models.Model):
    name = models.CharField(
        verbose_name=_("name"),
        help_text=_("Bắt buộc"),
        max_length=255,
    )

    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = _("Payment Selection")
        verbose_name_plural = _("Payment Selections")

    def __str__(self):
        return self.name
    
    
class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="checkout_addresses")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"
