import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

from .forms import LoginForm, SignUpForm
from .utils import get_documents_by_categories_tree
from .models import Document, Category


class IndexView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        documents_by_categories_tree = get_documents_by_categories_tree()
        return render(request, "index.html", {
            'documents_by_categories_tree': documents_by_categories_tree,
            'user': request.user
        })


class CategoryView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        category_id = kwargs['category_id']
        category_name = Category.objects.get(id=category_id).name
        category_documents = Document.objects.filter(category_id=category_id).values()
        return render(request, "category.html", {
            'category_name': category_name,
            'category_documents': category_documents,
        })


class DocumentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        document = Document.objects.get(id=kwargs['document_id'])
        return render(request, "document.html", {
            'document': {
                'Категория': document.category.name,
                'Наименование документа': document.name,
                'Файл документа': '',
                'Дата создания': document.created_at,
                'Дата обновления': document.updated_at,
            },
            'document_id': document.id,
            'document_code': document.code
        })


class SearchView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, "search.html", {})


class DownloadFileView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        document = Document.objects.get(id=kwargs['document_id'])
        file_path = document.file.path
        if os.path.exists(file_path):
            with open(file_path, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/msword")
                response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
                return response
        raise Http404


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


class ContactUsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        documents_by_categories_tree = get_documents_by_categories_tree()
        return render(request, "contact-us.html", {
            'documents_by_categories_tree': documents_by_categories_tree
        })
