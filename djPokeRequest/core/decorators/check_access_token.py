# django packages
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
# local packages
from djPokeRequest.core.exceptions.refugio_animales import DjRefugioAnimalesForbiddenError
from djPokeRequest.core.providers import RefugioAnimales


def verify_access_token(view_func):
    """
    Verifica que el access token se encuentre en las cookies del request, posteriormente se consulta un endpoint del api
    djRefugioAnimales para verificar el estado del token.

    Si el token no es valido se redirige a la vista de login para que introduzca de nuevo las credenciales
    :param view_func:
    :return:
    """
    def wrap(request, *args, **kwargs):
        MESSAGE_ERROR = "No se encuentra autentificado, por favor introduzca las credenciales para poder ver el " \
                        "recurso solicitado"
        REDIRECT_URL = reverse('login_djrefugioanimales_api')

        # Se valida que el access token se encuentre presente en las cookies del request
        if not request.COOKIES.get('access_token'):
            messages.error(request, MESSAGE_ERROR)
            return HttpResponseRedirect(REDIRECT_URL)

        # Se valida que el token sea correcto haciendo una peticion a la API
        api = RefugioAnimales(access_token=request.COOKIES.get('access_token'))
        try:
            access_token, refresh_token = api.verify_access_token(refresh=True)
            # Pasamos a las views los tokens para setearlos en la cookie por si se tuvieron que hacer refresh
            kwargs['cookies'] = {'access_token': access_token, 'refresh_token': refresh_token}
        except DjRefugioAnimalesForbiddenError:
            messages.error(request, MESSAGE_ERROR)
            return HttpResponseRedirect(REDIRECT_URL)

        # El access token esta presente en la peticion y no presenta ningun error
        return view_func(request, *args, **kwargs)
    return wrap
