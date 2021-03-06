import grequests
import requests


#region poke-errors
class PokeResourceEmptyError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "PokeResourceEmptyError: {}".format(self.value)
class PokeResourceNotAllowedError(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "PokeResourceNotAllowedError: {}".format(self.value)
        return "PokePaginationError: {}".format(self.value)
#endregion







class PokeRequest(object):
    # Ruta base del API
    HOST = "https://pokeapi.co/api/v2/"
    # Resources
    RESOURCE = {
        "pokemon": "pokemon",
        "species": "pokemon-species",
        "type":    "type",
    }

    def __init__(self, resource, identifier=None, page=None, limit=None):
        self.resource = resource  # Resource name
        self.identifier = identifier # identifier for the resources (id or name)
        self.page = page
        self.limit = limit # Pagination limit

        self.count = None
        self.next_page = None
        self.prev_page = None


    def __str__(self):
        return ("<PokeRequest"
            + " host='{}'"
            + ", resource='{}'"
            + ", identifier='{}'"
            + ", limit={}"
            + ", count={}"
            + ", next_page={}"
            + ", prev_page={}"
            + ">"
        ).format(
            self.HOST,
            self.resource,
            self.identifier,
            self.limit,
            self.count,
            self.next_page,
            self.prev_page,
        )



    def build_pagination_params(self):
        params = {}
        if self.page and isinstance(self.page, int):
            params["limit"] = self.limit or 10
            params["offset"] = (self.page - 1) * self.limit
        return params
        

    
    
    def get_full_request_url(self):
        """
        Construye la url para consultar la api segun los atributos de la clase
        """
        request_url, params = self.HOST, self.build_pagination_params()
        try:
            # resource
            if self.resource:
                if self.resource in self.RESOURCE:
                    request_url += "{}/".format(self.RESOURCE[self.resource])
                else: raise PokeResourceNotAllowedError("resource: '{}' is not allowed".format(self.resource))
            else: raise PokeResourceEmptyError("'resource' is required")
            # identifier if it exist
            if self.identifier: 
                request_url += "{}/".format(self.identifier)
        except (PokeResourceEmptyError, PokeResourceNotAllowedError) as ex:
            raise
        except Exception as ex:
            print ex
        return request_url, params
        

    def update_meta_pagination(self, response):
        if response != None:
            res = response.json()
            self.count = res["count"]
            self.next_page = res["next"]
            self.prev_page = res["previous"]


    def _get(self, url, params={}):
        response = None
        try:
            response = requests.get(url, params)
        except Exception as ex: print ex
        
        if response != None and response.status_code != 200:
            return None

        # Elemento especifico
        if not self.identifier:
            self.update_meta_pagination(response)

        return response


    def get(self):
        url, params = self.get_full_request_url()
        print "<Request url='{}', params='{}'>".format(url, params)
        return self._get(url, params)








class PokeRequestAsync(PokeRequest):
    
    def get_pokemon_with_picture_async(self):
        # Valor de retorno
        pokemon_response = []
        # Consulta del listado de pokemones
        response = super(PokeRequestAsync, self).get()
        pokemon_urls = []
        if response != None:
            # Extraccion de urls individuales
            for pokemon in response.json().get("results", []):
                pokemon_urls.append(pokemon["url"])
            # async request
            rs = (grequests.get(u) for u in pokemon_urls)        
            pokemon_list_res = grequests.map(rs)
            for res in pokemon_list_res:
                pokemon = res.json()
                
                name = pokemon.get("name", "")
                sprites = pokemon.get("sprites", None)
                url = None
                if sprites: url = sprites.get("front_default", None)
                
                pokemon_response.append({ "name": name, "sprite_url": url })
        return pokemon_response




    def get_pokemon_by_varieties_with_picture_async(self):
        # Valor de retorno
        pokemon_response = []
        # Consulta del listado de pokemones
        response = super(PokeRequestAsync, self).get()
        pokemon_urls = []
        if response != None:
            # Extraccion de urls individuales
            for pokemon in response.json().get("varieties", []):
                pokemon_urls.append(pokemon["pokemon"]["url"])
            # async request
            rs = (grequests.get(u) for u in pokemon_urls)        
            pokemon_list_res = grequests.map(rs)
            for res in pokemon_list_res:
                pokemon = res.json()
                
                name = pokemon.get("name", "")
                sprites = pokemon.get("sprites", None)
                url = None
                if sprites: url = sprites.get("front_default", None)
                
                pokemon_response.append({ "name": name, "sprite_url": url })
        return pokemon_response



    def get_pokemon_by_type_with_picture_async(self):
        # Valor de retorno
        pokemon_response = []
        # Consulta del listado de pokemones
        response = super(PokeRequestAsync, self).get()
        pokemon_urls = []
        if response != None:
            # Extraccion de urls individuales
            for pokemon in response.json().get("pokemon", []):
                pokemon_urls.append(pokemon["pokemon"]["url"])
            # async request
            rs = (grequests.get(u) for u in pokemon_urls)        
            pokemon_list_res = grequests.map(rs)
            for res in pokemon_list_res:
                pokemon = res.json()
                
                name = pokemon.get("name", "")
                sprites = pokemon.get("sprites", None)
                url = None
                if sprites: url = sprites.get("front_default", None)
                
                pokemon_response.append({ "name": name, "sprite_url": url })
        return pokemon_response