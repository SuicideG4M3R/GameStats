from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from logged.forms import LoginForm


class LoginView(View):
    def get(self, request):
        form = LoginForm()
        return render(request, 'add_form.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                next = request.GET.get('next', 'home')
                return redirect(next)
        return render(request, 'add_form.html', {'form': form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
