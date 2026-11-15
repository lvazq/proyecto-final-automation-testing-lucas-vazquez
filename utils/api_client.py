"""
api_client.py

Cliente HTTP reutilizable para las pruebas de API. Envuelve a
requests.Session para: usar siempre la misma URL base, aplicar un
timeout y registrar en el log cada petición (método, URL, status, tiempo).
"""

import requests

from utils.config import URL_BASE_API
from utils.logger import obtener_logger

logger = obtener_logger(__name__)


class ApiClient:
    """Cliente simple para consumir una API REST."""

    def __init__(self, url_base=URL_BASE_API, timeout=15):
        self.url_base = url_base.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Accept": "application/json",
                # Algunas APIs públicas rechazan el User-Agent por defecto de requests
                "User-Agent": "Mozilla/5.0 (compatible; proyecto-final-qa/1.0)",
            }
        )

    def _request(self, metodo, endpoint, **kwargs):
        url = f"{self.url_base}{endpoint}"
        logger.info(f"API {metodo} {url} | datos: {kwargs.get('json') or kwargs.get('params') or '-'}")
        respuesta = self.session.request(metodo, url, timeout=self.timeout, **kwargs)
        logger.info(
            f"API respuesta: {respuesta.status_code} en "
            f"{respuesta.elapsed.total_seconds():.2f}s"
        )
        return respuesta

    def get(self, endpoint, **kwargs):
        return self._request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self._request("POST", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self._request("DELETE", endpoint, **kwargs)
