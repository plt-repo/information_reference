from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from documents.views import IndexView, SearchView, LoginView, RegisterView, LogoutView, DocumentView, ContactUsView, \
    DownloadFileView, CategoryView, RegisterSuccess

admin.site.site_header = 'Админ-панель'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('category/<str:category_id>/', CategoryView.as_view(), name='category'),
    path('document/<str:document_id>/', DocumentView.as_view(), name='document'),
    path('download/<str:document_id>/', DownloadFileView.as_view(), name='download'),
    path('search', SearchView.as_view(), name='search'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('register', RegisterView.as_view(), name='register'),
    path('register-success', RegisterSuccess.as_view(), name='register_success'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('contact-us', ContactUsView.as_view(), name='contact_us'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
