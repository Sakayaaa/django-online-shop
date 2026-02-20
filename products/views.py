from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from django.http import JsonResponse
from .models import Category, Product, Brand
from checkout.models import CartItem


class CategoryList(View):
    def get(self, request, slug=None):
        if slug:
            parent = get_object_or_404(Category, slug=slug)
            children = parent.get_children()

            if not children.exists():
                return redirect(f"{reverse('products:product_list')}?category={parent.slug}")

            categories = children
            title = parent.name
        else:
            parent = None
            categories = Category.objects.filter(parent__isnull=True)
            title = 'Categories'

        return render(request, 'products/categories.html', {
            'categories': categories,
            'parent': parent,
            'page_title': title
        })


class ProductList(View):
    def get(self, request):
        category_slug = request.GET.get('category')
        brand_slug = request.GET.get('brand')

        products = Product.objects.all()
        category = None
        brand = None

        all_categories = Category.objects.all().order_by('tree_id', 'lft')
        brands = Brand.objects.all()

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            descendants = category.get_descendants(include_self=True)
            products = products.filter(category__in=descendants)

        if brand_slug:
            brand = get_object_or_404(Brand, slug=brand_slug)
            products = products.filter(brand=brand)

        context = {
            'products': products,
            'category': category,
            'brand': brand,
            'all_categories': all_categories,
            'brands': brands,
        }

        return render(request, 'products/product_list.html', context)


class ProductDetail(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        cart_quantity = 0

        if request.user.is_authenticated:
            cart_quantity = (
                CartItem.objects
                .filter(cart__user=request.user, product=product)
                .values_list("quantity", flat=True)
                .first()
                or 0
            )

        return render(request, 'products/product_detail.html', {
            'product': product,
            'cart_quantity': cart_quantity,
        })


class BrandsByCategory(View):
    def get(self, request):
        category_slug = request.GET.get('category')
        brands_qs = Brand.objects.all()

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            descendants = category.get_descendants(include_self=True)
            brands_qs = Brand.objects.filter(product__category__in=descendants).distinct()

        data = list(brands_qs.values('name', 'slug'))
        return JsonResponse(data, safe=False)
