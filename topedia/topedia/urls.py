# 2101940 Kyle Keene-Welch
# urls.py
# Main url file for the routes that can be accessed. Includes other sub url files when the url begins with prefix.

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('base.urls')),
    path('api/', include('base.api.urls'))
]

# Sets media folder as default for user files
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)