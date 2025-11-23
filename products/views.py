from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from .models import Category


class Categories(View):
    def get(self, request, slug=None):
        if slug:
            parent = get_object_or_404(Category, slug=slug)
            children = parent.get_children()

            if not children.exists():
                return redirect('products:list') + f'?category={parent.slug}'

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

    def post(self, request):
        pass
