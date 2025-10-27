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
        if not request.user.is_authenticated:
            return redirect('login')
        addresses = request.user.addresses.all()
        return render(request, 'accounts/view-profile.html', {'addresses': addresses})
# -------------------------------------------------------------------------------------------------------


class EditProfile(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('login')
        form = EditProfileForm(instance=request.user)
        addresses = request.user.addresses.all()
        return render(request, 'accounts/edit-profile.html', {'form': form, 'addresses': addresses})

    def post(self, request):
        form = EditProfileForm(request.POST, instance=request.user)
        addresses_data = list(zip(
            request.POST.getlist('city[]'),
            request.POST.getlist('street[]'),
            request.POST.getlist('number[]'),
            request.POST.getlist('postal_code[]')
        ))

        if form.is_valid():
            form.save()

            request.user.addresses.all().delete()
            for data in addresses_data[:5]:
                city, street, number, postal_code = [x.strip() for x in data]
                if any([city, street, number, postal_code]):
                    Address.objects.create(
                        user=request.user,
                        city=city,
                        street=street,
                        number=number,
                        postal_code=postal_code
                    )

            messages.success(request, "Profile updated successfully.")
            return redirect('profile')

        messages.error(request, "Something went wrong.")
        addresses = request.user.addresses.all()
        return render(request, 'accounts/edit-profile.html', {'form': form, 'addresses': addresses})
# -------------------------------------------------------------------------------------------------------
