# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm, PasswordResetForm
from django.contrib.auth import get_user_model
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

class SignInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password'}))
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

class SignupForm(UserCreationForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']

# class PassResetForm(PasswordResetForm):
    # captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())

class UpdatePass(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']

class UserInfoUpdate(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = get_user_model()  # Kullanıcı modeli (CustomUser)
        fields = ['first_name', 'last_name', 'email']