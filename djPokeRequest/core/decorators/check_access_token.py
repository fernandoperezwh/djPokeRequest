# coding=utf-8
# django packages
from django.conf import settings
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
# local packages
from djPokeRequest.core.exceptions.refugio_animales import DjRefugioAnimalesForbiddenError, \
    DjRefugioAnimalesRefreshTokenError, DjRefugioAnimalesServerConnectionError
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

        # Si el proyecto corre sobre la api publica de djRefugiAnimales entonces no tiene sentido seguir con las demas
        # validaciones. Por lo tanto, mandamos directamente a llamar la funcion
        if settings.DJREFUGIOANIMALES.get('is_public_api'):
            return view_func(request, *args, **kwargs)

        # Se valida que el access token se encuentre presente en las cookies del request
        if not request.COOKIES.get('access_token'):
            messages.warning(request, MESSAGE_ERROR)
            return HttpResponseRedirect(REDIRECT_URL)

        # Se valida que el token sea correcto haciendo una peticion a la API
        api = RefugioAnimales(access_token=request.COOKIES.get('access_token'),
                              refresh_token=request.COOKIES.get('refresh_token'))
        try:
            access_token, refresh_token = api.verify_access_token(refresh=True)
            # Pasamos en la view la instancia actualizada del cliente RefugioAnimales
            kwargs['api_tokens'] = {
                'access_token': access_token,
                'refresh_token': refresh_token,
            }
        except (DjRefugioAnimalesForbiddenError, DjRefugioAnimalesRefreshTokenError):
            messages.warning(request, MESSAGE_ERROR)
            return HttpResponseRedirect(REDIRECT_URL)
        except DjRefugioAnimalesServerConnectionError:
            messages.error(request, 'No ha sido posible establecer conexión con el servidor.')
            return HttpResponseRedirect(REDIRECT_URL)

        # El access token esta presente en la peticion y no presenta ningun error
        return view_func(request, *args, **kwargs)
    return wrap
