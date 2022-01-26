# django packages
from django.shortcuts import render


def render_with_cookie_setter(request, template_path, context, cookies={}):
    """
    Metodo django.shortcuts.render personalizado para setear cookies
    :param request:
    :param template_path:
    :param context:
    :param cookies:
    :return:
    """
    response = render(request, template_path, context)
    #
    for key, value in cookies.iteritems():
        response.set_cookie(key, value)
    return response
