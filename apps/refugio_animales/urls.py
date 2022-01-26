# coding=utf-8
# django packages
from django.conf.urls import url
# local packages
from apps.refugio_animales import views

urlpatterns = [
    url(r'^djRefugioAnimales/login/$', views.login, name='login_djrefugioanimales_api'),
    # region CRUD mascotas
    url(r'^pets/list/$', views.pets_list, name='pets_list'),
    url(r'^pets/delete/(\d+)/$', views.pets_delete, name='pets_delete'),
    # endregion
    # region CRUD dueños/dueñas de mascotas
    url(r'^owner/list/$', views.owners_list, name='owners_list'),
    url(r'^owner/delete/(\d+)/$', views.owners_delete, name='owners_delete'),
    # endregion
    # region CRUD vacunas
    url(r'^vaccines/list/$', views.vaccines_list, name='vaccines_list'),
    url(r'^vaccines/delete/(\d+)/$', views.vaccines_delete, name='vaccines_delete'),
    # endregion
]
