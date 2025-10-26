from django.shortcuts import render
from django.views import View
from .forms import RegisterForm
from django.shortcuts import redirect


class Login(View):
    def post(self, request):
        pass

    def get(self, request):
        return render(request, 'accounts/login.html', {})
# -------------------------------------------------------------------------------------------------------


class Logout(View):
    def post(self, request):
        pass

    def get(self, request):
        return render(request, 'accounts/logout.html', {})
# -------------------------------------------------------------------------------------------------------


class Register(View):
    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form':form})
# -------------------------------------------------------------------------------------------------------


class ViewProfile(View):
    def post(self, request):
        pass

    def get(self, request):
        return render(request, 'accounts/view-profile.html', {})
# -------------------------------------------------------------------------------------------------------


class EditProfile(View):
    def post(self, request):
        pass

    def get(self, request):
        return render(request, 'accounts/edit-profile.html', {})
# -------------------------------------------------------------------------------------------------------
