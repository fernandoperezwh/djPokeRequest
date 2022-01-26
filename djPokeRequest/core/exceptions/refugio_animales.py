# coding=utf-8
class DjRefugioAnimalesServerUnknowError(Exception):
    def __str__(self):
        return "DjRefugioAnimalesServerConnectionError: Ha ocurrido un error desconocido"


class DjRefugioAnimalesServerConnectionError(Exception):
    def __str__(self):
        return "DjRefugioAnimalesServerConnectionError: Un error ha ocurrido intentando conectar con el servidor"


class DjRefugioAnimalesAuthError(Exception):
    def __str__(self):
        return "DjRefugioAnimalesAuthError: Las credenciales proporcionadas son incorrectas"


class DjRefugioAnimalesRefreshTokenError(Exception):
    def __str__(self):
        return "DjRefugioAnimalesAuthError: El refresh_token no esta definido o es incorrecto"


class DjRefugioAnimalesForbiddenError(Exception):
    def __str__(self):
        return "DjRefugioAnimalesAuthError: No cuentas con el permiso para acceder al recurso"


class DjRefugioAnimalesNotFoundError(Exception):
    def __str__(self):
        return "DjRefugioAnimalesAuthError: No se encontro el recurso"


class DjRefugioAnimalesBadRequestError(Exception):
    def __str__(self):
        return "DjRefugioAnimalesAuthError: Verifique los datos de su petición, hay campos incorrectos"