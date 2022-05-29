from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.shortcuts import render, redirect

from .forms import LoginForm, SignUpForm


class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "index.html", {})


class SearchView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "search.html", {})


class LoginView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "login.html", {
            'next': request.GET['next'] if request.GET.get('next') else '/'
        })

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        next_page = request.POST['next_page'] if request.POST['next_page'] else '/'
        # check whether it's valid:
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(next_page)
            else:
                return render(request, "login.html", {
                    'next': next_page,
                    'errors': {
                        'username': '<ul class="errorlist"><li>Пользователь не найден! Пройдите регистрацию.</li></ul>'
                    }
                })
        else:
            return render(request, "login.html", {
                'next': next_page,
                'errors': form.errors
            })


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "register.html", {})

    def post(self, request, *args, **kwargs):
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
        else:
            return render(request, "register.html", {
                'errors': form.errors
            })


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
