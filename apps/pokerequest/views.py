from django.shortcuts import render
from django.http import HttpResponse, JsonResponse #, HttpResponseRedirect
# local imports
from apps.pokerequest.core.services.poke_api import PokeRequest, PokeRequestAsync


# Create your views here.
def welcome(request):
    return HttpResponse("welcome")



def pokemon_list(request):
    pr = PokeRequestAsync(resource=PokeRequest.RESOURCE["pokemon"], limit=5, offset=0)
    object_list = pr.get_pokemon_with_picture_async()
    return render(request, "pokemon_listado.html", {
        "object_list": object_list,
    })




def pokemon_detail(request, identifier):
    res_obj = None

    pr = PokeRequest(resource="pokemon", identifier=identifier)
    response = pr.get()
    if response != None:
        obj = response.json()

        ability_list = ", ".join( [ ele["ability"]["name"] for ele in obj.get("abilities") ] )
        move_list = ", ".join( [ ele["move"]["name"] for ele in obj.get("moves") ] )

        sprite_list = []
        for _, value in obj["sprites"].items():
            if isinstance(value, unicode):
                sprite_list.append(value)

        res_obj = {
            "name":      obj["name"],
            "sprites":   sprite_list,
            "weight" :   obj["weight"],
            "height" :   obj["height"],
            "species":   obj["species"]["name"],
            "abilities": ability_list,
            "moves":     move_list,
        }
    return render(request, "pokemon_detalle.html", {
        "object": res_obj,
    })


def pokemon_species_list(request, identifier=None):
    pr = PokeRequestAsync(resource="species", identifier=identifier)
    object_list = pr.get_pokemon_by_varieties_with_picture_async()
    return render(request, "pokemon_listado.html", {
        "object_list": object_list,
    })