from django.shortcuts import render
from django.http import HttpResponse, JsonResponse #, HttpResponseRedirect
# local imports
from apps.pokerequest.core.services.poke_api import PokeRequest, PokeRequestAsync


# Create your views here.

def pokemon_list(request):
    page = int(request.GET.get("page", 1))

    pr = PokeRequestAsync(resource=PokeRequest.RESOURCE["pokemon"], page=page, limit=10)
    object_list = pr.get_pokemon_with_picture_async()
    
    return render(request, "pokemon_listado.html", {
        "object_list": object_list,
        "pagination": {
            "page": page,
            "range": range(
                page - 1 if page > 1 else page,
                page + 2 if page > 1 else page + 3,
            ),
            "prev_page": page - 1 if page > 1 else page,
            "has_prev_page": page > 1,
            "has_next_page": True,
            "next_page": page + 1,
        }
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
            "types":     obj["types"],
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
    return render(request, "pokemon_especie_listado.html", {
        "specie_name": identifier,
        "object_list": object_list,
    })


def pokemon_types_list(request, identifier=None):
    pr = PokeRequestAsync(resource="type", identifier=identifier)
    object_list = pr.get_pokemon_by_type_with_picture_async()
    return render(request, "pokemon_tipo_listado.html", {
        "type_name": identifier,
        "object_list": object_list,
    })