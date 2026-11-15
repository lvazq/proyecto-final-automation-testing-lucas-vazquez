"""
inventory_page.py

Page Object de la página de inventario (listado de productos).
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait

from pages.base_page import BasePage


class InventoryPage(BasePage):
    """Acciones y elementos del catálogo de productos."""

    TITULO = (By.CLASS_NAME, "title")
    PRODUCTOS = (By.CLASS_NAME, "inventory_item")
    NOMBRES = (By.CLASS_NAME, "inventory_item_name")
    PRECIOS = (By.CLASS_NAME, "inventory_item_price")
    MENU = (By.ID, "react-burger-menu-btn")
    FILTRO_ORDEN = (By.CLASS_NAME, "product_sort_container")
    ICONO_CARRITO = (By.CLASS_NAME, "shopping_cart_link")
    CONTADOR_CARRITO = (By.CLASS_NAME, "shopping_cart_badge")

    # Valores del desplegable de orden: az, za, lohi (precio ↑), hilo (precio ↓)
    ORDEN_PRECIO_ASCENDENTE = "lohi"
    ORDEN_PRECIO_DESCENDENTE = "hilo"
    ORDEN_NOMBRE_ASCENDENTE = "az"
    ORDEN_NOMBRE_DESCENDENTE = "za"

    @staticmethod
    def _boton_de_producto(nombre_producto):
        """Locator del botón Add/Remove del producto con ese nombre."""
        return (
            By.XPATH,
            "//div[contains(@class,'inventory_item_name') "
            f"and normalize-space()='{nombre_producto}']"
            "/ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' inventory_item ')]"
            "//button",
        )

    def esta_cargada(self):
        self._esperar_visible(self.TITULO)
        return self

    def obtener_titulo(self):
        return self._obtener_texto(self.TITULO)

    def obtener_cantidad_productos(self):
        self._esperar_visible(self.PRODUCTOS)
        return len(self.driver.find_elements(*self.PRODUCTOS))

    def obtener_nombres(self):
        """Lista con los nombres de todos los productos, en el orden mostrado."""
        self._esperar_visible(self.NOMBRES)
        return [e.text for e in self.driver.find_elements(*self.NOMBRES)]

    def obtener_precios(self):
        """Lista de precios (float) de todos los productos, en el orden mostrado."""
        self._esperar_visible(self.PRECIOS)
        return [float(e.text.replace("$", "")) for e in self.driver.find_elements(*self.PRECIOS)]

    def obtener_primer_producto(self):
        """Devuelve {'nombre': ..., 'precio': ...} del primer producto listado."""
        nombre = self.obtener_nombres()[0]
        precio = self.driver.find_elements(*self.PRECIOS)[0].text
        self.logger.info(f"Primer producto: {nombre} - {precio}")
        return {"nombre": nombre, "precio": precio}

    def elementos_de_interfaz_visibles(self):
        """Devuelve un dict indicando si menú, filtro y carrito están visibles."""
        return {
            "menu": self._esta_visible(self.MENU),
            "filtro": self._esta_visible(self.FILTRO_ORDEN),
            "carrito": self._esta_visible(self.ICONO_CARRITO),
        }

    def ordenar_por(self, valor_orden):
        """Selecciona un criterio en el desplegable de orden (az, za, lohi, hilo)."""
        self.logger.info(f"Ordenando productos por '{valor_orden}'")
        desplegable = self._esperar_visible(self.FILTRO_ORDEN)
        Select(desplegable).select_by_value(valor_orden)

    def agregar_producto(self, nombre_producto):
        """Hace click en 'Add to cart' del producto indicado."""
        self.logger.info(f"Agregando al carrito: {nombre_producto}")
        self._hacer_click(self._boton_de_producto(nombre_producto))

    def quitar_producto(self, nombre_producto):
        """Hace click en 'Remove' del producto indicado (desde el inventario)."""
        self.logger.info(f"Quitando del carrito: {nombre_producto}")
        self._hacer_click(self._boton_de_producto(nombre_producto))

    def obtener_contador_carrito(self):
        """Número sobre el ícono del carrito (0 si el badge no existe)."""
        badges = self.driver.find_elements(*self.CONTADOR_CARRITO)
        return int(badges[0].text) if badges else 0

    def esperar_contador_carrito(self, cantidad_esperada, timeout=5):
        """Espera explícita a que el badge del carrito muestre la cantidad esperada."""
        WebDriverWait(self.driver, timeout).until(
            lambda _: self.obtener_contador_carrito() == cantidad_esperada
        )
        return self.obtener_contador_carrito()

    def ir_al_carrito(self):
        self.logger.info("Navegando al carrito")
        self._hacer_click(self.ICONO_CARRITO)
