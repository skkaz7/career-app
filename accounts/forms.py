from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class LoginForm(forms.Form):
    username = forms.CharField(max_length=64, label='', widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    password = forms.CharField(max_length=64,
                               label='',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Password'}))


class ChangePasswordForm(forms.Form):
    old_password = forms.CharField(max_length=64, widget=forms.PasswordInput)
    new_password = forms.CharField(max_length=64, widget=forms.PasswordInput)
    re_new_password = forms.CharField(max_length=64, widget=forms.PasswordInput)

    def clean(self):
        data = super(ChangePasswordForm, self).clean()
        if data['new_password'] != data['re_new_password']:
            raise ValidationError("Nowe hasła się nie zgadzają!")
        return data


class CreateUserForm(forms.ModelForm):
    password = forms.CharField(max_length=64, widget=forms.PasswordInput)
    re_password = forms.CharField(max_length=64, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username']
        help_texts = {
            'username': None
        }

    def clean(self):
        data = super(CreateUserForm, self).clean()
        if data['password'] != data['re_password']:
            raise ValidationError("Hasła się nie zgadzają!")
        return data
