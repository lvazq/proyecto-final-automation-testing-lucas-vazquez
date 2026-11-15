"""
test_login.py

Pruebas de login con datos externos (datos/login.csv).
Cubre el caso positivo y varios escenarios NEGATIVOS (usuario bloqueado,
credenciales inválidas, campos vacíos), todo con un único test parametrizado.
"""

import pytest

from pages.login_page import LoginPage
from utils.data_reader import leer_csv

pytestmark = pytest.mark.ui

CASOS_LOGIN = leer_csv("login.csv")


@pytest.mark.parametrize("caso", CASOS_LOGIN, ids=lambda caso: caso["caso"])
def test_login(driver, caso):
    """
    Ejecuta el login con cada fila del CSV y valida el resultado esperado:
    - 'exitoso': redirige a /inventory.html y muestra el título Products.
    - 'error': permanece en el login y muestra el mensaje de error esperado.
    """
    login = LoginPage(driver).abrir()
    login.login(caso["usuario"], caso["password"])

    if caso["resultado_esperado"] == "exitoso":
        login.esperar_inventario()
        assert "/inventory.html" in login.url_actual
        assert driver.title == "Swag Labs"
    else:
        assert login.obtener_mensaje_error() == caso["mensaje_error"]
        assert "/inventory.html" not in login.url_actual
