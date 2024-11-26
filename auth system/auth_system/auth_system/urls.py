"""django_website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from business_logic.WebSocket import routing

urlpatterns = [
    path("", include('users.urls')),
    path("", include('main.urls')),
    # custom admin dashboard
    path("", include('dashboard_admin.urls')),
    
    
    # path('ws/', include(routing.websocket_urlpatterns)),
    path('tinymce/', include('tinymce.urls')),
    path("", include("allauth.urls")), 
    # django admin
    path('admin/', admin.site.urls),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)