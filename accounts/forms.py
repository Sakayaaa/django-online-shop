from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm
from django import forms


class RegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email', required=False)

    class Meta():
        model = CustomUser
        fields = ['first_name', 'last_name', 'password1', 'password2', 'email']

        def save(self, commit=True):
            user = super().save(commit=False)
            user.email = self.cleaned_data['email']

            if commit:
                user.save()
            return user


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email']

