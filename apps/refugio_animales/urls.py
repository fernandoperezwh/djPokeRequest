# django packages
from django.conf.urls import url
# local packages
from apps.refugio_animales import views

urlpatterns = [
    url(r'^djRefugioAnimales/login/$', views.login, name='login_djrefugioanimales_api'),
    url(r'^pets/list/$', views.pets_list, name='pets_list'),
    # url(r'^owner/list/$', views.pets_list, name='owner_list'),
    # url(r'^vaccines/list/$', views.pets_list, name='vaccines_list'),
]
