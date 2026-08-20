from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    # Canlıda da medya (galeri/slider) sunulsun — static() DEBUG=false iken boş döner
    re_path(
        r'^media/(?P<path>.*)$',
        serve,
        {'document_root': str(settings.MEDIA_ROOT)},
    ),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
