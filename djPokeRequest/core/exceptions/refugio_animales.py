class DjRefugioAnimalesServerError(Exception):
    def __str__(self):
        return "DjRefugioAnimalesServerError: Un error ha ocurrido intentando conectar con el servidor"


class DjRefugioAnimalesAuthError(Exception):
    def __str__(self):
        return "DjRefugioAnimalesAuthError: Las credenciales proporcionadas son incorrectas"


class DjRefugioAnimalesRefreshTokenError(Exception):
    def __str__(self):
        return "DjRefugioAnimalesAuthError: El refresh_token no esta definido o es incorrecto"


class DjRefugioAnimalesForbiddenError(Exception):
    def __str__(self):
        return "DjRefugioAnimalesAuthError: No cuentas con el permiso para acceder al recurso"
