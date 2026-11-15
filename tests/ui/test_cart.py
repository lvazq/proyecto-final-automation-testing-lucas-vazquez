"""
test_cart.py

Pruebas del carrito: agregar productos (parametrizado con
datos/productos.json), verificar contador y contenido, y quitar un producto.
"""

import pytest

from pages.cart_page import CartPage
from utils.data_reader import leer_json

pytestmark = pytest.mark.ui

PRODUCTOS = leer_json("productos.json")


@pytest.mark.parametrize("nombre_producto", PRODUCTOS)
def test_agregar_producto_al_carrito(driver, pagina_inventario, nombre_producto):
    """Agrega un producto: el contador pasa a 1 y el producto aparece en el carrito."""
    assert pagina_inventario.obtener_contador_carrito() == 0

    pagina_inventario.agregar_producto(nombre_producto)
    assert pagina_inventario.esperar_contador_carrito(1) == 1

    pagina_inventario.ir_al_carrito()
    carrito = CartPage(driver).esta_cargada()

    assert carrito.esperar_cantidad_items(1) == 1
    assert carrito.producto_esta_en_carrito(nombre_producto)


def test_agregar_varios_productos_incrementa_contador(pagina_inventario):
    """Agregar todos los productos del JSON deja el contador en esa cantidad."""
    for nombre in PRODUCTOS:
        pagina_inventario.agregar_producto(nombre)

    assert pagina_inventario.esperar_contador_carrito(len(PRODUCTOS)) == len(PRODUCTOS)


def test_quitar_producto_del_carrito(driver, pagina_inventario):
    """Un producto agregado y luego quitado desde el carrito deja el carrito vacío."""
    producto = PRODUCTOS[0]
    pagina_inventario.agregar_producto(producto)
    pagina_inventario.esperar_contador_carrito(1)
    pagina_inventario.ir_al_carrito()

    carrito = CartPage(driver).esta_cargada()
    assert carrito.esperar_cantidad_items(1) == 1
    assert carrito.producto_esta_en_carrito(producto)

    carrito.quitar_producto(producto)
    assert carrito.esperar_cantidad_items(0) == 0
