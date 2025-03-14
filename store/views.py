from django.shortcuts import get_object_or_404, render

from .models import Category, Product
from common.service import service
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def product_all(request):
    products = Product.objects.prefetch_related('product_image').filter(is_active=True)

    # Lấy giá trị page trong request, nếu không có thì mặc định là 1
    page = request.GET.get('page', 1)

    products_paged = getPage(products, 10, page)

    context = {"products": products_paged}

    return render(request, "store/index.html", context)


def category_list(request, category_slug=None):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(
        category__in=Category.objects.get(slug=category_slug).get_descendants(include_self=True)
    )

    # Lấy giá trị page trong request, nếu không có thì mặc định là 1
    page = request.GET.get('page', 1)

    products_paged = getPage(products, 10, page)

    return render(request, "store/category.html", {"category": category, "products": products_paged})


def product_detail(request, slug):
    product = get_object_or_404(Product.objects.prefetch_related('product_specification'), slug=slug)
    descriptions = product.description.split("\r\n", -1)

    products_same_brand = Product.objects.prefetch_related('product_image').filter(brand=product.brand)[:10]
    products_similar = Product.objects.prefetch_related('product_image').filter(product_type=product.product_type)[:10]

    return render(request, "store/detail.html", {
        "product": product,
        "descriptions": descriptions,
        "products_same_brand": products_same_brand,
        "products_similar": products_similar
    })


def search(request):
    q = request.GET['q']
    value = service.change_to_slug(q)

    products = Product.objects.filter(Q(slug__icontains=value) | Q(title__icontains=q))

    # Lấy giá trị page trong request, nếu không có thì mặc định là 1
    page = request.GET.get('page', 1)

    products_paged = getPage(products, 10, page)

    return render(request, "store/search.html", {"products": products_paged, "q": q})


def getPage(items, numberItemsPerPage, currentPage):
    # Paging với số phần tử 1 trang là numberItemsPerPage
    paginator = Paginator(items, numberItemsPerPage)

    try:
        products_paged = paginator.page(currentPage)
    except PageNotAnInteger:
        products_paged = paginator.page(1)
    except EmptyPage:
        products_paged = paginator.page(paginator.num_pages)

    return products_paged
