from django import forms
from django.contrib.auth import (authenticate, get_user_model, login, logout)
from .models import Todo, TodoList


UserModel = get_user_model()


class UserLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': "form-control", "placeholder": "Email address"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control", "placeholder": "Password"}))

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise forms.ValidationError("This User does not exist")
            elif not user.check_password(password):
                raise forms.ValidationError("Password is incorrect")

            """
            if not user.is_active():
                raise forms.ValidationError("User is not active.")
            """
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistraionForm(forms.ModelForm):
    username = forms.CharField(required=True,
                               widget=forms.TextInput(attrs={'class': "form-control", "placeholder": "Username"}))
    password = forms.CharField(required=True,
                               widget=forms.PasswordInput(attrs={'class': "form-control", "placeholder": "Password"}))
    re_password = forms.CharField(required=True,
                                  widget=forms.PasswordInput(attrs={'class': "form-control",
                                                                    "placeholder": "Re-enter the Password"}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': "form-control", "placeholder": "Email Address"}))

    class Meta:
        model = UserModel
        fields = [
            "username",
            "email",
            "password",
        ]

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get("password")
        re_password = self.cleaned_data.get("re_password")
        email = self.cleaned_data.get("email")
        if not password == re_password:
            raise forms.ValidationError("Password does not match")
        email_qs = UserModel.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email already is use")
        return super(UserRegistraionForm, self).clean(*args, **kwargs)

