"""
test_inventory.py

Pruebas de navegación y catálogo: título, productos, elementos de
interfaz y ordenamiento por precio.
"""

import pytest

pytestmark = pytest.mark.ui


def test_titulo_y_productos_visibles(pagina_inventario):
    """El inventario muestra el título 'Products' y los 6 productos del catálogo."""
    assert pagina_inventario.obtener_titulo() == "Products"
    assert pagina_inventario.obtener_cantidad_productos() == 6


def test_elementos_de_interfaz_presentes(pagina_inventario):
    """Menú, filtro de orden y carrito están presentes en pantalla."""
    elementos = pagina_inventario.elementos_de_interfaz_visibles()
    assert elementos["menu"], "No se ve el menú hamburguesa"
    assert elementos["filtro"], "No se ve el filtro de ordenamiento"
    assert elementos["carrito"], "No se ve el ícono del carrito"


def test_listar_nombre_y_precio_del_primer_producto(pagina_inventario):
    """Obtiene nombre y precio del primer producto y valida su formato."""
    primero = pagina_inventario.obtener_primer_producto()
    assert primero["nombre"] != ""
    assert primero["precio"].startswith("$")


@pytest.mark.parametrize(
    "criterio, descendente",
    [("lohi", False), ("hilo", True)],
    ids=["precio_menor_a_mayor", "precio_mayor_a_menor"],
)
def test_ordenar_por_precio(pagina_inventario, criterio, descendente):
    """Tras ordenar por precio, la lista queda efectivamente ordenada."""
    pagina_inventario.ordenar_por(criterio)
    precios = pagina_inventario.obtener_precios()
    assert precios == sorted(precios, reverse=descendente)
