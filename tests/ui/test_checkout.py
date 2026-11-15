"""
test_checkout.py

Flujo completo de compra (login -> producto -> carrito -> checkout ->
confirmación) y escenarios negativos del formulario con datos de
datos/checkout.json.
"""

import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from utils.data_reader import leer_json

pytestmark = pytest.mark.ui

DATOS_CHECKOUT = leer_json("checkout.json")
PRODUCTO = leer_json("productos.json")[0]


def _llegar_al_formulario_de_checkout(driver, pagina_inventario):
    """Paso común: agrega un producto, va al carrito e inicia el checkout."""
    pagina_inventario.agregar_producto(PRODUCTO)
    pagina_inventario.esperar_contador_carrito(1)
    pagina_inventario.ir_al_carrito()
    CartPage(driver).esta_cargada().ir_a_checkout()
    return CheckoutPage(driver)


def test_checkout_completo_exitoso(driver, pagina_inventario):
    """Compra de punta a punta con datos válidos y mensaje de confirmación final."""
    checkout = _llegar_al_formulario_de_checkout(driver, pagina_inventario)

    datos = DATOS_CHECKOUT["datos_validos"]
    checkout.completar_datos(datos["nombre"], datos["apellido"], datos["codigo_postal"])
    checkout.continuar()
    checkout.esperar_resumen()
    checkout.finalizar()

    assert checkout.obtener_mensaje_confirmacion() == "Thank you for your order!"


@pytest.mark.parametrize(
    "caso", DATOS_CHECKOUT["casos_invalidos"], ids=lambda caso: caso["caso"]
)
def test_checkout_con_datos_incompletos(driver, pagina_inventario, caso):
    """ESCENARIO NEGATIVO: faltando un dato, se muestra el error y no avanza."""
    checkout = _llegar_al_formulario_de_checkout(driver, pagina_inventario)

    checkout.completar_datos(caso["nombre"], caso["apellido"], caso["codigo_postal"])
    checkout.continuar()

    assert checkout.obtener_mensaje_error() == caso["mensaje_error"]
    assert checkout.esta_en_paso_uno()
