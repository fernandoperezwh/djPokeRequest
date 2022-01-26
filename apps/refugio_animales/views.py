# coding=utf-8
# django packages
from django.contrib import messages
# local packages
from apps.refugio_animales.forms import DjRefugioAnimalesLoginForm
from djPokeRequest.core.decorators.check_access_token import verify_access_token
from djPokeRequest.core.exceptions.refugio_animales import DjRefugioAnimalesAuthError, DjRefugioAnimalesServerError
from djPokeRequest.core.providers import RefugioAnimales
from djPokeRequest.core.utils import render_with_cookie_setter


def login(request):
    success_login = False
    form = DjRefugioAnimalesLoginForm()

    if request.method == 'POST':
        form = DjRefugioAnimalesLoginForm(request.POST)
        if form.is_valid():
            api = RefugioAnimales()
            cleaned_data = form.cleaned_data
            try:
                # Se obtiene los tokens del acceso y posteriormente se establecen en las cookies si se pudo llevar  con
                # exito el login
                access_token, refresh_token = api.login(cleaned_data.get('username'), cleaned_data.get('password'))
                messages.success(request, "Inicio de sesión correcto, en breve se le redireccionara a la pagina de "
                                          "inicio")
                success_login = True  # Bandera para indicar que se guarden los tokens en las cookies
            except DjRefugioAnimalesAuthError:
                messages.error(request, "Credenciales incorrectas, por favor verifique el nombre de usuario y "
                                        "contraseña")
            except DjRefugioAnimalesServerError:
                messages.error(request, "Un error ha ocurrido intentando conectar con el servidor")
    # Si ocurrio un inicio de sesion exitoso se establecen los tokens en las cookies
    cookies = {'access_token': access_token, 'refresh_token': refresh_token } if success_login else {}

    return render_with_cookie_setter(
        request,
        template_path='login.html',
        context={'form': form,'success_login': success_login},
        cookies=cookies
    )


@verify_access_token
def pets_list(request, *args, **kwargs):
    api = RefugioAnimales(**kwargs.get('api_tokens', {}))
    try:
        response = api.get_pets()
    except DjRefugioAnimalesServerError:
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
def owner_list(request, *args, **kwargs):
    api = RefugioAnimales(**kwargs.get('api_tokens', {}))
    try:
        response = api.get_owner()
    except DjRefugioAnimalesServerError:
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
def vaccines_list(request, *args, **kwargs):
    api = RefugioAnimales(**kwargs.get('api_tokens', {}))
    try:
        response = api.get_vaccines()
    except DjRefugioAnimalesServerError:
        # se define una lista vacia y se regresa el mensaje de que el servidor tuvo un porblmea
        response = []
        messages.error(request, "Un error ha ocurrido intentando conectar con el servidor")

    return render_with_cookie_setter(
        request,
        template_path='vacuna_listado.html',
        context={'object_list': response},
        cookies=kwargs.get('api_tokens') if kwargs else {}
    )
