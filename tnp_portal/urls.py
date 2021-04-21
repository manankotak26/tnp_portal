"""tnp_portal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from . import views

urlpatterns = [
                  path('', TemplateView.as_view(template_name='home.html')),
                  path('contact', TemplateView.as_view(template_name='contact.html')),
                  path('placement', views.placement, name='placement'),
                  path('login/', views.login, name='login'),
                  path('student/', include('student.urls')),
                  path('tnp_admin/', include('tnp_admin.urls')),
                  path('forgotPassword', views.forgotPassword, name="forgotPassword"),
                  path('recover/', views.recover, name="recover"),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = 'tnp_admin.views.handler404'
handler500 = 'tnp_admin.views.handler500'

handler404 = 'student.views.handler404'
handler500 = 'student.views.handler500'

handler404 = 'tnp_portal.views.handler404'
handler500 = 'tnp_portal.views.handler500'
