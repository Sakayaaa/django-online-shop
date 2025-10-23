from django.shortcuts import render
from django.views import View


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
        pass

    def get(self, request):
        return render(request, 'accounts/register.html', {})
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
