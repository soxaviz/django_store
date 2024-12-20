from django.shortcuts import render, redirect
from .models import Product, Category, Subcategory, Review, Favorite
from django.core.paginator import Paginator
from .forms import ReviewForm


def home_view(request):
    return render(request, "pages/index.html")


def get_paginator(request, queryset):
    paginator = Paginator(queryset, 3)
    page = request.GET.get("page")
    result = paginator.get_page(page)
    return result


def shop_view(request):
    products = Product.objects.all()
    result = get_paginator(request, products)
    context = {
        "products": result
    }
    return render(request, "pages/shop.html", context)


def subcategory_articles_view(request, slug):
    subcategory = Subcategory.objects.get(slug=slug)
    products = Product.objects.filter(subcategory=subcategory)
    result = get_paginator(request, products)
    context = {
        "products": result
    }
    return render(request, "pages/shop.html", context)


def product_detail_view(request, slug):
    product = Product.objects.get(slug=slug)

    if request.method == "POST":
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.author = request.user
            review.product = product
            review.save()
            form = ReviewForm()

    else:
        form = ReviewForm()
    reviews = product.reviews.all()
    # try:
    # rating = sum([x.rating for x in reviews if x.rating]) / reviews.count()
    # except:
    #     rating = 0
    form = ReviewForm()
    context = {
        "product": product,
        'form': form,
        'reviews': reviews,
        # 'rating': round(rating, 1)

    }
    return render(request, "pages/product_detail.html", context)


def search(request):
    query = request.GET.get('q')
    products = Product.objects.filter(title__iregex=query)
    subcategories = Subcategory.objects.filter(title__iregex=query)
    if not query:
        products = []
        subcategories = []

    context = {
        "products": products,
        "subcategories": subcategories,

    }
    return render(request, 'pages/search_results.html', context)


def favorite_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    favorite_product = request.session.get('favorites')

    if favorite_product is None:
        favorite_product = []

    if favorite_product:
        products = Product.objects.filter(id__in=favorite_product)

    else:
        products = []

    context = {
        "products": products
    }
    return render(request, "pages/favorites.html", context)


def add_to_favorites(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    product = Product.objects.get(id=product_id)

    if 'favorites' not in request.session:
        request.session['favorites'] = []

    favorite_product = request.session['favorites']

    if product.id not in favorite_product:
        favorite_product.append(product.id)
        request.session['favorites'] = favorite_product

    return redirect('favorites')


def remove_from_favorites(request, product_id):
    if not request.user.is_authenticated:
        return redirect('login')

    product = Product.objects.get(id=product_id)

    if 'favorites' not in request.session:
        request.session['favorites'] = []

    favorite_product = request.session['favorites']

    if product.id in favorite_product:
        favorite_product.remove(product.id)
    request.session['favorites'] = favorite_product

    return redirect('favorites')
