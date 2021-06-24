from django.conf.urls import url
# local imports
from apps.pokerequest import views


urlpatterns = [
    url(r'^index$', views.welcome),
    
    url(r'^pokemon/list/$', views.pokemon_list),
    url(r'^pokemon-species/([-\w]+)/list/$', views.pokemon_species_list),
    url(r'^pokemon-type/([-\w]+)/list/$', views.pokemon_types_list),
    url(r'^pokemon/([-\w]+)/detail/$', views.pokemon_detail),
]
