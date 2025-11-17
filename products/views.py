from django.shortcuts import render
from django.views import View
from .models import Category

class Categories(View):
    def get(self, request):
        root_categories = Category.objects.filter(parent__isnull=True)
        return render(request, 'products/categories.html', {'root_categories':root_categories})
    
    def post(self, request):
        pass