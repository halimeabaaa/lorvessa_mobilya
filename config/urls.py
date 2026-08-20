from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('pages.urls')),
    re_path(
        r'^static/media/(?P<path>.*)$',
        serve,
        {'document_root': str(settings.MEDIA_ROOT)},
    ),
    re_path(
        r'^media/(?P<path>.*)$',
        serve,
        {'document_root': str(settings.MEDIA_ROOT)},
    ),
]

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
