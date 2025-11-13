from django.shortcuts import render
from django.views import View

class Categories(View):
    def get(self, request):
        return render(request, 'products/categories.html', {})
    
    def post(self, request):
        pass