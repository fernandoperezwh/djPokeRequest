# django packages
from django.contrib import messages
from django.http import HttpResponseRedirect
# local packages
from djPokeRequest.core.exceptions.refugio_animales import DjRefugioAnimalesForbiddenError, \
    DjRefugioAnimalesServerUnknowError, DjRefugioAnimalesServerConnectionError
from djPokeRequest.core.utils import render_with_cookie_setter


def generic_api_delete(request, delete_function, instance, redirect, cookies={}, custom_messages={}):
    """
    Funcion generica para eliminar registros mediante llama a api

    :param request: Django Request Object
    :param delete_function: Metodo del provider RefugioAnimales a llamar para eliminar el registro
    :param instance: Datos del registro
    :param redirect: url name a redireccionar
    :param cookies: Diccionario de cookies para setear
    :param custom_messages: Diccionario de imagenes personalizados del error
    :return:
    """
    DEFAULT_SUCCESS_MESSAGE = "Se elimino el registro correctamente."
    DEFAULT_FORBIDDEN_ERROR_MESSAGE = 'No cuenta con los permisos para eliminar este registro'
    DEFAULT_UNKNOW_ERROR_MESSAGE = 'Ha ocurrido un error desconocido'
    DEFAULT_CONNECTION_ERROR_MESSAGE = 'Un error ha ocurrido intentando conectar con el servidor'

    if request.method == "POST":
        try:
            # Se ejecuta el metodo para eliminar algun registro de djRefugioAnimales
            delete_function(instance.get('id'))
            messages.success(request, custom_messages.get('success') or DEFAULT_SUCCESS_MESSAGE)
            return HttpResponseRedirect(redirect)
        except DjRefugioAnimalesForbiddenError:
            messages.error(request, custom_messages.get('forbidden_error', DEFAULT_FORBIDDEN_ERROR_MESSAGE))
            return HttpResponseRedirect(redirect)
        except DjRefugioAnimalesServerUnknowError:
            messages.error(request, custom_messages.get('unknow_error', DEFAULT_UNKNOW_ERROR_MESSAGE))
            return HttpResponseRedirect(redirect)
        except DjRefugioAnimalesServerConnectionError:
            messages.error(request, custom_messages.get('connection_error', DEFAULT_CONNECTION_ERROR_MESSAGE))
            return HttpResponseRedirect(redirect)

    return render_with_cookie_setter(
        request,
        template_path='generic_delete.html',
        context={'object': instance, 'redirect': redirect},
        cookies=cookies
    )