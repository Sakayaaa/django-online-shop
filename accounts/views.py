from django.shortcuts import render
from django.views import View

class Login(View):
    def post(self, request):
        pass
    
    def get(self, request):
        return render(request, 'accounts/login.html', {})