# coding=utf-8
# django packages
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse
# local packages
from apps.refugio_animales.forms import DjRefugioAnimalesLoginForm
from djPokeRequest.core.decorators.check_access_token import verify_access_token
from djPokeRequest.core.exceptions.refugio_animales import DjRefugioAnimalesAuthError, \
    DjRefugioAnimalesServerConnectionError, DjRefugioAnimalesNotFoundError, DjRefugioAnimalesForbiddenError
from djPokeRequest.core.providers import RefugioAnimales
from djPokeRequest.core.utils import render_with_cookie_setter, generic_api_delete


def login(request):
    SUCCESS_LOGIN_MESSAGE = "Inicio de sesión correcto, en breve se le redireccionara a la pagina de inicio"
    success_login = False
    form = DjRefugioAnimalesLoginForm()

    # Antes de realizar el inicio de sesion se verifica que los tokens de la cookie sean validos
    api = RefugioAnimales(access_token=request.COOKIES.get('access_token'),
                          refresh_token=request.COOKIES.get('refresh_token'))
    try:
        access_token, refresh_token = api.verify_access_token(refresh=True)
        messages.success(request, SUCCESS_LOGIN_MESSAGE)
        return render_with_cookie_setter(
            request,
            template_path='login.html',
            context={'form': form, 'success_login': True},
            cookies={'access_token': access_token, 'refresh_token': refresh_token}
        )
    except (DjRefugioAnimalesServerConnectionError, DjRefugioAnimalesForbiddenError):
        # No se pudo realizar el login con los tokens de la cookie
        pass


    if request.method == 'POST':
        form = DjRefugioAnimalesLoginForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            try:
                # Se obtiene los tokens del acceso y posteriormente se establecen en las cookies si se pudo llevar  con
                # exito el login
                access_token, refresh_token = api.login(cleaned_data.get('username'), cleaned_data.get('password'))
                messages.success(request, SUCCESS_LOGIN_MESSAGE)
                success_login = True  # Bandera para indicar que se guarden los tokens en las cookies
            except DjRefugioAnimalesAuthError:
                messages.error(request, "Credenciales incorrectas, por favor verifique el nombre de usuario y "
                                        "contraseña")
            except DjRefugioAnimalesServerConnectionError:
                messages.error(request, "Un error ha ocurrido intentando conectar con el servidor")
    # Si ocurrio un inicio de sesion exitoso se establecen los tokens en las cookies
    cookies = {'access_token': access_token, 'refresh_token': refresh_token } if success_login else {}

    return render_with_cookie_setter(
        request,
        template_path='login.html',
        context={'form': form,'success_login': success_login},
        cookies=cookies
    )


# region CRUD mascotas
@verify_access_token
def pets_list(request, *args, **kwargs):
    api = RefugioAnimales(**kwargs.get('api_tokens', {}))
    try:
        response = api.get_pets()
    except DjRefugioAnimalesForbiddenError:
        return HttpResponseRedirect(reverse('login_djrefugioanimales_api'))
    except DjRefugioAnimalesServerConnectionError:
        # se define una lista vacia y se regresa el mensaje de que el servidor tuvo un porblmea
        response = []
        messages.error(request, "Un error ha ocurrido intentando conectar con el servidor")

    return render_with_cookie_setter(
        request,
        template_path='mascota_listado.html',
        context={'object_list': response, 'root_img': api.base_endpoint},
        cookies=kwargs.get('api_tokens', {}) if kwargs else {}
    )


@verify_access_token
def pets_delete(request, pk, *args, **kwargs):
    RETURN_URL = 'pets_list'
    api = RefugioAnimales(**kwargs.get('api_tokens', {}))

    # Se intenta obtener el registro a eliminar
    try:
        instance = api.get_pet(pk)
    except DjRefugioAnimalesNotFoundError:
        messages.warning(request, 'No se encontro la mascota con el id #{pk}'.format(pk=pk))
        return HttpResponseRedirect(reverse(RETURN_URL))

    # Se manda a llamar las instrucciones genericas para eliminar en base al funcionamiento del api
    return generic_api_delete(
        request=request,
        delete_function=api.delete_pet,
        instance=instance,
        redirect=reverse(RETURN_URL),
    )
# endregion


# region CRUD dueños/dueñas de mascotas
@verify_access_token
def owners_list(request, *args, **kwargs):
    api = RefugioAnimales(**kwargs.get('api_tokens', {}))
    try:
        response = api.get_owners()
    except DjRefugioAnimalesForbiddenError:
        return HttpResponseRedirect(reverse('login_djrefugioanimales_api'))
    except DjRefugioAnimalesServerConnectionError:
        # se define una lista vacia y se regresa el mensaje de que el servidor tuvo un porblmea
        response = []
        messages.error(request, "Un error ha ocurrido intentando conectar con el servidor")

    return render_with_cookie_setter(
        request,
        template_path='persona_listado.html',
        context={'object_list': response},
        cookies=kwargs.get('api_tokens') if kwargs else {}
    )


@verify_access_token
def owners_delete(request, pk, *args, **kwargs):
    RETURN_URL = 'owners_list'
    api = RefugioAnimales(**kwargs.get('api_tokens', {}))

    # Se intenta obtener el registro a eliminar
    try:
        instance = api.get_owner(pk)
    except DjRefugioAnimalesNotFoundError:
        messages.warning(request, 'No se encontró el/la dueño/dueña con el id #{pk}'.format(pk=pk))
        return HttpResponseRedirect(reverse(RETURN_URL))

    # Se manda a llamar las instrucciones genericas para eliminar en base al funcionamiento del api
    return generic_api_delete(
        request=request,
        delete_function=api.delete_owner,
        instance=instance,
        redirect=reverse(RETURN_URL)
    )
# endregion


# region CRUD vacunas
@verify_access_token
def vaccines_list(request, *args, **kwargs):
    api = RefugioAnimales(**kwargs.get('api_tokens', {}))
    try:
        response = api.get_vaccines()
    except DjRefugioAnimalesForbiddenError:
        return HttpResponseRedirect(reverse('login_djrefugioanimales_api'))
    except DjRefugioAnimalesServerConnectionError:
        # se define una lista vacia y se regresa el mensaje de que el servidor tuvo un porblmea
        response = []
        messages.error(request, "Un error ha ocurrido intentando conectar con el servidor")

    return render_with_cookie_setter(
        request,
        template_path='vacuna_listado.html',
        context={'object_list': response},
        cookies=kwargs.get('api_tokens') if kwargs else {}
    )


@verify_access_token
def vaccines_delete(request, pk, *args, **kwargs):
    RETURN_URL = 'vaccines_list'
    api = RefugioAnimales(**kwargs.get('api_tokens', {}))

    # Se intenta obtener el registro a eliminar
    try:
        instance = api.get_vaccine(pk)
    except DjRefugioAnimalesNotFoundError:
        messages.warning(request, 'No se encontro la vacuna con el id #{pk}'.format(pk=pk))
        return HttpResponseRedirect(reverse(RETURN_URL))

    # Se manda a llamar las instrucciones genericas para eliminar en base al funcionamiento del api
    return generic_api_delete(
        request=request,
        delete_function=api.delete_vaccine,
        instance=instance,
        redirect=reverse(RETURN_URL)
    )
# endregion