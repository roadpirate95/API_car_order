from django.contrib import admin
from django.urls import path, include
from .yasg import doc_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('carsapp.urls')),
]

urlpatterns += doc_urls
