# coding=utf-8
# django packages
from django.conf import settings
# thrid party packages
import requests
# local packages
from djPokeRequest.core.exceptions.refugio_animales import DjRefugioAnimalesAuthError, \
    DjRefugioAnimalesServerConnectionError, DjRefugioAnimalesForbiddenError, DjRefugioAnimalesRefreshTokenError, \
    DjRefugioAnimalesServerUnknowError, DjRefugioAnimalesNotFoundError, DjRefugioAnimalesBadRequestError

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

    def __get_resource(self, endpoint):
        """
        Funcion generica que consulta algun recurso.
        Si un error ocurre esta funcion generica maneja los errores
        :param endpoint: Endpoint del recurso
        :return:
        """
        try:
            response = requests.get(endpoint, headers=self.headers)
            if response.status_code == 404:
                raise DjRefugioAnimalesNotFoundError
            if response.status_code == 401:
                raise DjRefugioAnimalesForbiddenError
            return response.json()
        except CONNECTION_ERROR:
            raise DjRefugioAnimalesServerConnectionError

    def __create_resource(self, endpoint, payload):
        """
        Funcion generica que crea nuevo registro en un recurso especifico.
        Si un error ocurre esta funcion generica maneja los errores
        :param endpoint: Endpoint del recurso
        :param payload: Campos del formulario para crear este nuevo registro
        :return:
        """
        try:
            response = requests.post(endpoint, data=payload, headers=self.headers)
            # Error por body incorrecto del request
            if response.status_code == 400:
                raise DjRefugioAnimalesBadRequestError
            # Error en permisos
            if response.status_code == 401:
                raise DjRefugioAnimalesForbiddenError
            # verifica algun error desconocido
            if response.status_code != 201:
                raise DjRefugioAnimalesServerUnknowError
            # En este punto pudo editar correctamente el registro
            return
        except CONNECTION_ERROR:
            raise DjRefugioAnimalesServerConnectionError

    def __edit_resource(self, endpoint, payload):
        """
        Funcion generica que edita un registro de un recurso especifico.
        Si un error ocurre esta funcion generica maneja los errores
        :param endpoint: Endpoint del recurso
        :param payload: Campos del formulario para crear este nuevo registro
        :return:
        """
        try:
            response = requests.put(endpoint, data=payload, headers=self.headers)
            # Error por body incorrecto del request
            if response.status_code == 400:
                # NOTE: Podria especificarse los campos para dar información al cliene
                raise DjRefugioAnimalesBadRequestError
            # Error en permisos
            if response.status_code == 401:
                raise DjRefugioAnimalesForbiddenError
            # Elemento no encontrado
            if response.status_code == 404:
                raise DjRefugioAnimalesNotFoundError
            # verifica algun error desconocido
            if response.status_code != 200:
                raise DjRefugioAnimalesServerUnknowError
            # En este punto pudo editar correctamente el registro
            return
        except CONNECTION_ERROR:
            raise DjRefugioAnimalesServerConnectionError

    def __delete_resource(self, endpoint):
        """
        Funcion generica que elimina un recurso en especifico.
        Si un error ocurre esta funcion generica maneja los errores
        :param endpoint: Endpoint del recurso
        :return:
        """
        try:
            response = requests.delete(endpoint, headers=self.headers)
            if response.status_code == 401:
                raise DjRefugioAnimalesForbiddenError
            if response.status_code == 404:
                raise DjRefugioAnimalesNotFoundError
            # verifica algun error desconocido
            if response.status_code != 204:
                raise DjRefugioAnimalesServerUnknowError
            # En este punto pudo eliminar correctamente el registro
            return
        except CONNECTION_ERROR:
            raise DjRefugioAnimalesServerConnectionError

    def verify_access_token(self, refresh=False):
        """
        Verifica el estado del access_token consultando a la API. Si el token no es valido se levantara un raise del
        tipo DjRefugioAnimalesForbiddenError indicando que el token es invalido.

        En caso contrario el metodo terminara con exito sin retornar ningun valor.

        :param refresh: Indica si consulta el servicio para hacer refresh del access_token y obtener uno valido
        :return: Regresa una tupla donde el primer elemento corresponde al access_token y el segundo al refresh_token
        """
        ENDPOINT = "{endpoint}/verify/".format(endpoint=self.auth_endpoint)
        if not self.access_token:
            raise DjRefugioAnimalesForbiddenError
        try:
            response = requests.post(ENDPOINT, data={
                'token': self.access_token
            })
            # Comprueba el status code de la respuesta para validar si el access_token es incorrecto
            if response.status_code == 401:
                # Si no esta habilitado el refresh_token entonces levantamos directamente la excepcion
                if not refresh:
                    raise DjRefugioAnimalesForbiddenError
                # La bandera de refresh esta activa. Por lo tanto intentamos hacer el refresh
                self.refresh_access_token()
            return self.access_token, self.refresh_token
        except CONNECTION_ERROR:
            raise DjRefugioAnimalesServerConnectionError

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
            return self.access_token, self.refresh_token
        except CONNECTION_ERROR:
            raise DjRefugioAnimalesServerConnectionError

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
            raise DjRefugioAnimalesServerConnectionError

    def get_pet(self, pk):
        """
        Obtiene el registro de una mascota mediante su pk consultando la API de djRefugioAnimales
        :param pk: Id del registro de mascota a eliminar
        :return:
        """
        ENDPOINT = "{endpoint}/mascota/{pk}/".format(endpoint=self.api_endpoint, pk=pk)
        return self.__get_resource(ENDPOINT)

    def get_pets(self):
        """
        Obtiene la lista de mascotas consultando la API de djRefugioAnimales
        :return:
        """
        ENDPOINT = "{endpoint}/mascota/".format(endpoint=self.api_endpoint)
        return self.__get_resource(ENDPOINT)

    def create_pet(self, payload):
        """
        Crea un nuevo registro de la mascota consultando la API de djRefugioAnimales
        """
        ENDPOINT = "{endpoint}/mascota/".format(endpoint=self.api_endpoint)
        self.__create_resource(ENDPOINT, payload)

    def edit_pet(self, pk, payload):
        """
        Edita un registro de la mascota por su id consultando la API de djRefugioAnimales
        """
        ENDPOINT = "{endpoint}/mascota/{pk}/".format(endpoint=self.api_endpoint, pk=pk)
        self.__edit_resource(ENDPOINT, payload)

    def delete_pet(self, pk):
        """
        Elimina un registro de la mascota por su id consultando la API de djRefugioAnimales
        """
        ENDPOINT = "{endpoint}/mascota/{pk}/".format(endpoint=self.api_endpoint, pk=pk)
        self.__delete_resource(ENDPOINT)

    def get_vaccine(self, pk):
        """
        Obtiene el registro de una mascota mediante su pk consultando la API de djRefugioAnimales
        :param pk: Id del registro de mascota a eliminar
        :return:
        """
        ENDPOINT = "{endpoint}/vacuna/{pk}/".format(endpoint=self.api_endpoint, pk=pk)
        return self.__get_resource(ENDPOINT)

    def get_vaccines(self):
        """
        Obtiene la lista de vacunas consultando la API de djRefugioAnimales
        :return:
        """
        ENDPOINT = "{endpoint}/vacuna/".format(endpoint=self.api_endpoint)
        return self.__get_resource(ENDPOINT)

    def create_vaccine(self, payload):
        """
        Crea un nuevo registro de vacuna consultando la API de djRefugioAnimales
        """
        ENDPOINT = "{endpoint}/vacuna/".format(endpoint=self.api_endpoint)
        self.__create_resource(ENDPOINT, payload)

    def edit_vaccine(self, pk, payload):
        """
        Edita un registro de vacuna por su id consultando la API de djRefugioAnimales
        """
        ENDPOINT = "{endpoint}/vacuna/{pk}/".format(endpoint=self.api_endpoint, pk=pk)
        self.__edit_resource(ENDPOINT, payload)

    def delete_vaccine(self, pk):
        """
        Elimina un registro de vacuna por su id consultando la API de djRefugioAnimales
        """
        ENDPOINT = "{endpoint}/vacuna/{pk}/".format(endpoint=self.api_endpoint, pk=pk)
        self.__delete_resource(ENDPOINT)

    def get_owner(self, pk):
        """
        Obtiene el registro de un dueño/dueña mediante su pk consultando la API de djRefugioAnimales
        :param pk: Id del registro de mascota a eliminar
        :return:
        """
        ENDPOINT = "{endpoint}/persona/{pk}/".format(endpoint=self.api_endpoint, pk=pk)
        return self.__get_resource(ENDPOINT)

    def get_owners(self):
        """
        Obtiene la lista de dueños/dueñas de mascotas consultando la API de djRefugioAnimales
        :return:
        """
        ENDPOINT = "{endpoint}/persona/".format(endpoint=self.api_endpoint)
        return self.__get_resource(ENDPOINT)

    def create_owner(self, payload):
        """
        Crea un nuevo registro del dueño/dueña de mascota consultando la API de djRefugioAnimales
        """
        ENDPOINT = "{endpoint}/persona/".format(endpoint=self.api_endpoint)
        self.__create_resource(ENDPOINT, payload)

    def edit_owner(self, pk, payload):
        """
        Edita un registro del dueño/dueña de mascota por su id consultando la API de djRefugioAnimales
        """
        ENDPOINT = "{endpoint}/persona/{pk}/".format(endpoint=self.api_endpoint, pk=pk)
        self.__edit_resource(ENDPOINT, payload)

    def delete_owner(self, pk):
        """
        Elimina un registro del dueño/dueña de la mascota por su id consultando la API de djRefugioAnimales
        """
        ENDPOINT = "{endpoint}/persona/{pk}/".format(endpoint=self.api_endpoint, pk=pk)
        self.__delete_resource(ENDPOINT)
