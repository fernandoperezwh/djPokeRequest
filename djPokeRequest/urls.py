"""djPokeRequest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.views.static import serve 

# local imports
from apps.pokerequest.views import pokemon_list
from djPokeRequest import settings

urlpatterns = [
    url(r'^$', pokemon_list),
    url(r'^pr/', include('apps.pokerequest.urls')),
    url(r'^ra/', include('apps.refugio_animales.urls')),
]
urlpatterns += [
    url(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}), 
]
