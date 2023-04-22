from django.contrib import admin
from django.urls import path, include

from .yasg import urlpatterns as yasg_doc

urlpatterns = [
    path('admin/', admin.site.urls),
    path('developers/', include('developers.urls')),
]
urlpatterns += yasg_doc
