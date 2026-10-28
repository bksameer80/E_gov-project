from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from certificates import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home_view, name='apply'),
    path('track/', views.track_view, name='track'),
    path('verify/<uuid:cert_uuid>/', views.verify_view, name='verify'),
    path('certificate/<uuid:cert_uuid>/', views.print_certificate, name='print_certificate'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)