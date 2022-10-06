from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse

from accounts.forms import LoginForm, ChangePasswordForm, CreateUserForm


class LoginView(View):

    def get(self, request):
        return render(request, 'login.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                url = request.GET.get('next', reverse('base'))
                return redirect(url)
        return render(request, 'login.html', {'form': LoginForm(), 'message': 'Logowanie nie powiodło się!'})


class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('base')


class ChangePasswordView(View):
    def get(self, request):
        form = ChangePasswordForm()
        return render(request, 'change_password.html', {'form': form})

    def post(self, request):
        form = ChangePasswordForm(request.POST)
        user = request.user
        old_password = request.POST.get('old_password')
        if user.check_password(old_password):
            if form.is_valid():
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                return redirect(reverse('login'))
            return render(request, 'change_password.html', {'form': form})
        else:
            return render(request, 'change_password.html', {'form': form, 'message': "Stare hasło jest błędne!"})


class RegisterView(View):
    def get(self, request):
        form = CreateUserForm()
        return render(request, 'register.html', {'form': form})

    def post(self, request):
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect(reverse('login'))
        return render(request, 'register.html', {'form': form})
