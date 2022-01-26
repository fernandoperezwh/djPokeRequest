# coding=utf-8
# django packages
from django.conf import settings
# thrid party packages
import requests
# local packages
from djPokeRequest.core.exceptions.refugio_animales import DjRefugioAnimalesAuthError, DjRefugioAnimalesServerError, \
    DjRefugioAnimalesForbiddenError, DjRefugioAnimalesRefreshTokenError


CONNECTION_ERROR = (
    requests.ConnectTimeout,
    requests.ConnectionError,
)


class RefugioAnimales:
    is_public_api = settings.DJREFUGIOANIMALES.get('is_public_api')
    host = settings.DJREFUGIOANIMALES.get('host')
    port = settings.DJREFUGIOANIMALES.get('port')

    def __init__(self, access_token=None, refresh_token=None):
        self.access_token = access_token
        self.refresh_token = refresh_token

    @property
    def base_endpoint(self):
        """
        Endpoint base de djRefugioAnimales
        """
        return "{host}:{port}".format(host=self.host, port=self.port)

    @property
    def api_endpoint(self):
        """
        Endpoint base de la API djRefugioAnimales
        """
        base_endpoint = "{host}:{port}/api".format(host=self.host, port=self.port)
        if not self.is_public_api:
            # En caso de que la api que vamos a consumir no sea la publica agregamos el '/priv'
            base_endpoint += '/priv'
        return base_endpoint

    @property
    def auth_endpoint(self):
        """
        Endpoint base para autentificación de API djRefugioAnimales
        """
        return "{endpoint}/api/auth".format(endpoint=self.base_endpoint)

    @property
    def headers(self):
        api_headers = {}
        # Se agrega el header de 'Authorization' si la consulta se realiza sobre la api privada
        if not self.is_public_api:
            api_headers['Authorization'] = 'Bearer {access_token}'.format(access_token=self.access_token)
        return api_headers

    def verify_access_token(self, refresh=False):
        """
        Verifica el estado del access_token consultando a la API. Si el token no es valido se levantara un raise del
        tipo DjRefugioAnimalesForbiddenError indicando que el token es invalido.

        En caso contrario el metodo terminara con exito sin retornar ningun valor.

        :param refresh: Indica si consulta el servicio para hacer refresh del access_token y obtener uno valido
        :return: Regresa una tupla donde el primer elemento corresponde al access_token y el segundo al refresh_token
        """
        ENDPOINT = "{endpoint}/verify".format(endpoint=self.auth_endpoint)
        if not self.access_token:
            raise DjRefugioAnimalesForbiddenError
        try:
            response = requests.get(ENDPOINT)
            # Comprueba el status code de la respuesta para validar si el access_token es incorrecto
            if response.status_code == 401:
                # Si no esta habilitado el refresh_token entonces levantamos directamente la excepcion
                if not refresh:
                    raise DjRefugioAnimalesForbiddenError
                # La bandera de refresh esta activa. Por lo tanto intentamos hacer el refresh
                self.refresh_access_token()
            return self.access_token, self.refresh_token
        except CONNECTION_ERROR:
            raise DjRefugioAnimalesServerError

    def refresh_access_token(self):
        """
        Realiza el refresh del access_token.

        :return: Regresa una tupla donde el primer elemento corresponde al access_token y el segundo al refresh_token
        """
        ENDPOINT = "{endpoint}/refresh/".format(endpoint=self.auth_endpoint)
        # Se comprueba si el refresh_token se encuentra definido
        if not self.refresh_token:
            raise DjRefugioAnimalesRefreshTokenError
        # Consultamos el recurso para refrescar el access_token
        try:
            response = requests.post(ENDPOINT, data={
                'refresh': self.refresh_token
            })
            # El refresh_token es incorrecto
            if response.status_code == 401:
                raise DjRefugioAnimalesRefreshTokenError
            # En este punto se pudo obtener un nuevo access_token
            response_data = response.json()
            self.access_token = response_data.get('access')
            self.refresh_token = response_data.get('refresh')
            return self.access_token, self.refresh_tokens
        except CONNECTION_ERROR:
            raise DjRefugioAnimalesServerError

    def login(self, username, password):
        """
        Realiza la autentificacion de un usuario admin de Django mediante username y password

        :param username: User name perteneciente a usuario admin de django
        :param password: Password perteneciente a usuario admin de django
        :return: Regresa una tupla donde el primer elemento corresponde al access_token y el segundo al refresh_token
        """
        ENDPOINT = "{endpoint}/".format(endpoint=self.auth_endpoint)
        try:
            response = requests.post(ENDPOINT, data={
                'username': username,
                'password': password,
            })
            # Credenciales invalidas
            if response.status_code != 200:
                raise DjRefugioAnimalesAuthError
            response_data = response.json()
            # Inicio de sesión exitoso, retornamos los dos tokens
            self.access_token = response_data.get('access')
            self.refresh_token = response_data.get('refresh')
            return self.access_token, self.refresh_token
        except CONNECTION_ERROR:
            raise DjRefugioAnimalesServerError

    def get_pets(self):
        """
        Obtiene la lista de mascotas consultando la API de djRefugioAnimales
        :return:
        """
        ENDPOINT = "{endpoint}/mascota/".format(endpoint=self.api_endpoint)
        try:
            response = requests.get(ENDPOINT, headers=self.headers)
            if response.status_code == 401:
                raise DjRefugioAnimalesForbiddenError
            return response.json()
        except CONNECTION_ERROR:
            raise DjRefugioAnimalesServerError

    def get_vaccines(self):
        """
        Obtiene la lista de vacunas consultando la API de djRefugioAnimales
        :return:
        """
        ENDPOINT = "{endpoint}/vacuna/".format(endpoint=self.api_endpoint)
        try:
            response = requests.get(ENDPOINT, headers=self.headers)
            if response.status_code == 401:
                raise DjRefugioAnimalesForbiddenError
            return response.json()
        except CONNECTION_ERROR:
            raise DjRefugioAnimalesServerError

    def get_owner(self):
        """
        Obtiene la lista de dueños de mascotas consultando la API de djRefugioAnimales
        :return:
        """
        ENDPOINT = "{endpoint}/persona/".format(endpoint=self.api_endpoint)
        try:
            response = requests.get(ENDPOINT, headers=self.headers)
            if response.status_code == 401:
                raise DjRefugioAnimalesForbiddenError
            return response.json()
        except CONNECTION_ERROR:
            raise DjRefugioAnimalesServerError
