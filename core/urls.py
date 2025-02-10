from django.contrib import admin
from django.urls import path, include, re_path
from django.views.static import serve

from core import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('playlist.urls')),
    re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT,
                                              'show_indexes': settings.DEBUG}),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT,
                                             'show_indexes': settings.DEBUG}),
]
