from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import View
from .models import Category, Product


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
        products = Product.objects.all()
        category = None
        all_categories = Category.objects.all().order_by('tree_id', 'lft')

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            descendants = category.get_descendants(include_self=True)
            products = products.filter(category__in=descendants)

        context = {
            'products': products,
            'category': category,
            'all_categories': all_categories,
        }

        return render(request, 'products/product_list.html', context)


class ProductDetail(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)

        return render(request, 'products/product_detail.html', {
            'product': product
        })
