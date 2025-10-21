from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect



urlpatterns = [
    path('', lambda request: redirect('accounts:login')),  # 👈 Redirect root to login
    path('accounts/', include('accounts.urls')),
    path('checker/', include('checker.urls')),
    path('admin/', admin.site.urls),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)