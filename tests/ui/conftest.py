"""
conftest.py (UI)

Fixtures exclusivas de las pruebas de interfaz:
- driver: abre y cierra el navegador en cada test.
- pagina_inventario: deja la sesión iniciada y devuelve el InventoryPage,
  para los tests que parten de "ya estoy logueado".
"""

import pytest

from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage
from utils.config import PASSWORD_VALIDO, USUARIO_VALIDO
from utils.driver_factory import crear_driver
from utils.logger import obtener_logger

logger = obtener_logger(__name__)


@pytest.fixture
def driver():
    """Navegador Chrome nuevo para cada test; se cierra siempre al terminar."""
    logger.info("Iniciando navegador")
    navegador = crear_driver()
    yield navegador
    logger.info("Cerrando navegador")
    navegador.quit()


@pytest.fixture
def pagina_inventario(driver):
    """Hace login con el usuario válido y devuelve la página de inventario lista."""
    login = LoginPage(driver)
    login.abrir()
    login.login(USUARIO_VALIDO, PASSWORD_VALIDO)
    login.esperar_inventario()
    return InventoryPage(driver).esta_cargada()
