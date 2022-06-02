import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.contrib.admin.models import LogEntry, ACTION_FLAG_CHOICES

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
            'title': f'САНАЭксперт | {category_name}'
        })


class DocumentView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        document = Document.objects.get(id=kwargs['document_id'])
        doc_change_history = [{
            'action_time': change_info.action_time,
            'change_message': change_info.get_change_message()
        } for change_info in LogEntry.objects.filter(content_type_id=9, object_id=document.id)
        ]
        return render(request, "document.html", {
            'document': {
                'Категория': document.category.name,
                'Наименование документа': document.name,
                'Файл документа': '',
                'Дата создания': document.created_at,
                'Дата обновления': document.updated_at,
            },
            'document_id': document.id,
            'document_code': document.code,
            'title': f'САНАЭксперт | {document.code}',
            'doc_change_history': doc_change_history
        })


class SearchView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        categories = {category['id']: category['name'] for category in Category.objects.values('id', 'name')}

        return render(request, "search.html", {
            'title': f'САНАЭксперт | Поиск документов',
            'categories': categories,
            'ordering_fields': {
                'code': 'Обозначение документа',
                'name': 'Наименование документа',
                'created_at': 'Дата создания',
                'updated_at': 'Дата обновления',
            },
            'documents': []
        })

    def post(self, request, *args, **kwargs):
        categories = request.POST.getlist('categories')
        sort_order = request.POST['sort_order']
        ordering_field = request.POST['ordering_field']
        search_text = request.POST['search_text']
        if categories:
            queryset_name = Document.objects.filter(name__icontains=search_text, category_id__in=categories)
            queryset_code = Document.objects.filter(code__icontains=search_text, category_id__in=categories)
        else:
            queryset_name = Document.objects.filter(name__icontains=search_text)
            queryset_code = Document.objects.filter(code__icontains=search_text)
        queryset = queryset_name.union(queryset_code).order_by(f"{sort_order}{ordering_field}")
        documents = [{
            'id': document.id,
            'code': document.code,
            'Категория': document.category.name,
            'Наименование документа': document.name,
            'Файл документа': '',
            'Дата создания': document.created_at,
            'Дата обновления': document.updated_at,
        } for document in queryset.all()]
        categories_for_select = {category['id']: category['name'] for category in Category.objects.values('id', 'name')}

        return render(request, "search.html", {
            'title': f'САНАЭксперт | Поиск документов',
            'categories': categories_for_select,
            'ordering_fields': {
                'code': 'Обозначение документа',
                'name': 'Наименование документа',
                'created_at': 'Дата создания',
                'updated_at': 'Дата обновления',
            },
            'documents': documents,
            'search_text': search_text,
            'selected_categories': {int(category) for category in categories}
        })


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
            'next': request.GET['next'] if request.GET.get('next') else '/',
            'title': 'САНАЭксперт | Авторизация'
        })

    def post(self, request, *args, **kwargs):
        key_translate = {
            'username': 'Логин',
            'password': 'Пароль',
        }
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
                        'Логин/Пароль': 'Ваша учетная запись не активирована!'
                    }
                })
        else:
            return render(request, "login.html", {
                'next': next_page,
                'errors': {key_translate[key]: error for key, error in form.errors.items()},
                'title': 'САНАЭксперт | Авторизация'
            })


class RegisterView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "register.html", {
            'title': 'САНАЭксперт | Регистрация'
        })

    def post(self, request, *args, **kwargs):
        key_translate = {
            'username': 'Логин',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'password1': 'Пароль',
            'password2': 'Повторите пароль',
        }
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data.get('username')
            # raw_password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=raw_password)
            # login(request, user)
            return redirect('register_success')
        else:
            return render(request, "register.html", {
                'errors': {key_translate[key]: error for key, error in form.errors.items()},
                'title': 'САНАЭксперт | Регистрация'
            })


class RegisterSuccess(View):
    def get(self, request, *args, **kwargs):
        return render(request, "register-success.html", {
            'title': 'САНАЭксперт | Успешная регистрация'
        })


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')


class ContactUsView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        documents_by_categories_tree = get_documents_by_categories_tree()
        return render(request, "contact-us.html", {
            'documents_by_categories_tree': documents_by_categories_tree,
            'title': 'САНАЭксперт | Поддержка'
        })
