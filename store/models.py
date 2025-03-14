from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    name = models.CharField(
        verbose_name=_("Tên danh mục:"),
        help_text=_("Bắt buộc và duy nhất"),
        max_length=255,
        unique=True,
    )
    slug = models.SlugField(verbose_name=_("Slug"), max_length=255, unique=True)
    # image = models.ImageField(
    #     verbose_name=_("Ảnh"),
    #     help_text=_("Upload ảnh sản phẩm"),
    #     upload_to="images/",
    #     default="images/default.png",
    # )
    parent = TreeForeignKey("self", verbose_name=_("Danh mục cha"), on_delete=models.CASCADE, null=True, blank=True, related_name="children")
    is_active = models.BooleanField(verbose_name=_("Trạng thái hoạt động"), default=True)

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    def get_absolute_url(self):
        return reverse("store:category_list", args=[self.slug])

    def __str__(self):
        return self.name


class ProductType(models.Model):
    name = models.CharField(verbose_name=_("Loại sản phẩm"), help_text=_("Bắt buộc"), max_length=255, unique=True)
    is_active = models.BooleanField(verbose_name=_("Trạng thái hoạt động"), default=True)

    class Meta:
        verbose_name = _("Product Type")
        verbose_name_plural = _("Product Types")

    def __str__(self):
        return self.name


class ProductSpecification(models.Model):
    """
        The Product Specification Table contains product specification or features for the product types.
    """

    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name=_("Thông số"), help_text=_("Bắt buộc"), max_length=255)

    class Meta:
        verbose_name = _("Product Specification")
        verbose_name_plural = _("Product Specifications")

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    The Product table containing all product items.
    """

    product_type = models.ForeignKey(ProductType, verbose_name=_("loại sản phẩm"), on_delete=models.RESTRICT)
    category = models.ForeignKey(Category, verbose_name=_("danh mục"), on_delete=models.RESTRICT)
    title = models.CharField(
        verbose_name=_("Tên sản phẩm"),
        help_text=_("Bắt buộc"),
        max_length=255,
    )
    brand = models.CharField(
        verbose_name=_("Hãng sản phẩm"),
        help_text=_("Bắt buộc"),
        max_length=255,
        default=''
    )
    description = models.TextField(verbose_name=_("mô tả"), help_text=_("Không bắt buộc"), blank=True)
    slug = models.SlugField(max_length=255)
    regular_price = models.DecimalField(
        verbose_name=_("Giá gốc"),
        help_text=_("Tối đa 999.999.999đ"),
        error_messages={
            "name": {
                "max_length": _("Giá phải nằm trong khoảng từ 0 đến 999.999.999đ"),
            },
        },
        max_digits=9,
        decimal_places=0,
    )
    discount_price = models.DecimalField(
        verbose_name=_("Giảm giá"),
        help_text=_("Tối đa 999.999.999đ"),
        error_messages={
            "name": {
                "max_length": _("Giá phải nằm trong khoảng từ 0 đến 999.999.999đ"),
            },
        },
        max_digits=9,
        decimal_places=0,
    )
    is_active = models.BooleanField(
        verbose_name=_("Hiển thị sản phẩm"),
        help_text=_("Thay đổi chế độ hiển thị sản phẩm"),
        default=True,
    )
    created_at = models.DateTimeField(_("Created at"), auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(_("Updated at"), auto_now=True)
    users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="user_wishlist", blank=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _("Product")
        verbose_name_plural = _("Products")

    def get_absolute_url(self):
        return reverse("store:product_detail", args=[self.slug])

    def __str__(self):
        return self.title


class ProductSpecificationValue(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_specification")
    specification = models.ForeignKey(ProductSpecification, verbose_name=_("Thông số"), on_delete=models.RESTRICT)
    value = models.CharField(
        verbose_name=_("Giá trị"),
        help_text=_("Product specification value (maximum of 255 words"),
        max_length=255,
    )

    class Meta:
        verbose_name = _("Product Specification Value")
        verbose_name_plural = _("Product Specification Values")

    def __str__(self):
        return self.value


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_image")
    image = models.ImageField(
        verbose_name=_("Ảnh"),
        help_text=_("Upload ảnh sản phẩm"),
        upload_to="images",
        default="images/default.png",
    )
    alt_text = models.CharField(
        verbose_name=_("Tên ảnh"),
        help_text=_("Thêm tên ảnh"),
        max_length=255,
        null=True,
        blank=True,
    )
    is_feature = models.BooleanField(verbose_name=_("Ảnh avatar"), default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _("Product Image")
        verbose_name_plural = _("Product Images")
