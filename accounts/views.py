from django.forms import ValidationError
from django.shortcuts import render
from django.views import View
from .forms import RegisterForm, EditProfileForm, StyledPasswordChangeForm
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Address
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import update_session_auth_hash


class Login(View):
    def get(self, request):
        list(messages.get_messages(request))
        if request.user.is_authenticated:
            return redirect('profile')
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


@method_decorator(login_required, name='dispatch')
class Logout(View):
    def get(self, request):
        logout(request)
        list(messages.get_messages(request))
        return redirect('login')
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
        return render(request, 'accounts/edit-profile.html', {
            'form': form,
            'addresses': addresses
        })

    def post(self, request):
        form = EditProfileForm(request.POST, instance=request.user)
        list(messages.get_messages(request))

        addresses_data = list(zip(
            request.POST.getlist('city[]'),
            request.POST.getlist('street[]'),
            request.POST.getlist('number[]'),
            request.POST.getlist('postal_code[]'),
        ))

        if form.is_valid():
            form.save()

            valid_addresses = []
            errors_found = False

            for data in addresses_data[:5]:
                city, street, number, postal_code = [x.strip() for x in data]
                if all([city, street, number, postal_code]):
                    addr = Address(
                        user=request.user,
                        city=city,
                        street=street,
                        number=number,
                        postal_code=postal_code
                    )
                    try:
                        addr.full_clean()
                        valid_addresses.append(addr)
                    except ValidationError as e:
                        for field, errors in e.message_dict.items():
                            for err in errors:
                                messages.error(request, f"{field.replace('_', ' ').title()}: {err}")
                        errors_found = True

            if not errors_found:
                request.user.addresses.all().delete()
                for addr in valid_addresses:
                    addr.save()
                messages.success(request, "Profile updated successfully!")
                return redirect('profile')

        else:
            messages.error(request, "Please correct the errors below.")

        addresses = request.user.addresses.all()
        return render(request, 'accounts/edit-profile.html', {
            'form': form,
            'addresses': addresses
        })
# -------------------------------------------------------------------------------------------------------


@method_decorator(login_required, name='dispatch')
class ChangePassword(View):
    def get(self, request):
        form = StyledPasswordChangeForm(request.user)
        return render(request, 'accounts/change-password.html', {'form': form})

    def post(self, request):
        form = StyledPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('profile')

        else:
            return render(request, 'accounts/change-password.html', {'form': form})
