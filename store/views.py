from django.shortcuts import render, get_object_or_404
from store.models import Product
from category.models import category
from carts.models import CartItem
from carts.views import _cart_id
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
from django.db.models import Q
# Create your views here.


def store(request, category_slug=None):
    categories = None
    product = None
    if category_slug is not None:
        categories = get_object_or_404(category, slug=category_slug)
        product = Product.objects.filter(category=categories, is_available=True)
        paginator = Paginator(product, 1)
        page = request.GET.get('page')
        pagePaginator = paginator.get_page(page)
        product_count = product.count()
    else:
        product = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(product, 3)
        page = request.GET.get('page')
        pagePaginator = paginator.get_page(page)
        product_count = product.count()
    context = {'product': pagePaginator, 'product_count': product_count}
    return render(request, 'store/store.html', context)


def product_details(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e
    context = {'single_product': single_product, 'in_cart': in_cart}

    return render(request, 'store/product_details.html', context)


def search(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            product = Product.objects.filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            product_count = product.count()
    context = {'product': product, 'product_count': product_count}
    return render(request, 'store/store.html', context)
