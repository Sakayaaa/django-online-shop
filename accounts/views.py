from django.shortcuts import render
from django.views import View
from .forms import RegisterForm, EditProfileForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Address


class Login(View):
    def get(self, request):
        return render(request, 'accounts/login.html', {})

    def post(self, request):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(
                request, 'The given email or password is incorrect!')
            return redirect('login')
# -------------------------------------------------------------------------------------------------------


class Logout(View):
    def get(self, request):
        return render(request, 'accounts/logout.html', {})

    def post(self, request):
        pass
# -------------------------------------------------------------------------------------------------------


class Register(View):
    def get(self, request):
        form = RegisterForm()
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
        return render(request, 'accounts/register.html', {'form': form})
# -------------------------------------------------------------------------------------------------------


class ViewProfile(View):
    def get(self, request):
        return render(request, 'accounts/view-profile.html', {})

    def post(self, request):
        pass
# -------------------------------------------------------------------------------------------------------


class EditProfile(View):
    def get(self, request):
        user = request.user

        if not user.is_authenticated:
            return redirect('login')

        form = EditProfileForm(instance=user)
        addresses = user.addresses.all()

        return render(request, 'accounts/edit-profile.html', {'form': form, 'adresses': addresses})

    def post(self, request):
        user = request.user
        form = EditProfileForm(request.POST, instance=user)
        addresses = request.POST.getlist('addresses[]')

        if form.is_valid():
            form.save()

            request.user.addresses.all().delete()
            for addr in addresses[:5]:
                if addr.strip():
                    Address.objects.create(user=user, address=addr.strip())

            messages.success(request, "Profile Updated Successfuly")
            return redirect('profile')

        messages.error(request, 'Something Went Wrong!')
        return render(request, 'accounts/edit-profile.html', {'form': form})

# -------------------------------------------------------------------------------------------------------
