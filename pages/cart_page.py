"""
cart_page.py

Page Object de la página del carrito de compras.
"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class CartPage(BasePage):
    """Acciones y elementos del carrito."""

    LISTA = (By.CLASS_NAME, "cart_list")
    ITEMS = (By.CLASS_NAME, "cart_item")
    NOMBRES = (By.CLASS_NAME, "inventory_item_name")
    BOTON_CHECKOUT = (By.ID, "checkout")

    @staticmethod
    def _boton_quitar(nombre_producto):
        """Locator del botón 'Remove' del producto indicado dentro del carrito."""
        return (
            By.XPATH,
            "//div[contains(@class,'inventory_item_name') "
            f"and normalize-space()='{nombre_producto}']"
            "/ancestor::div[contains(concat(' ', normalize-space(@class), ' '), ' cart_item ')]"
            "//button",
        )

    def esta_cargada(self):
        """Espera a estar en /cart.html y a que la lista del carrito se haya renderizado."""
        self.esperar_url_contiene("/cart.html")
        self._esperar_visible(self.LISTA)
        return self

    def obtener_nombres(self):
        """Lista con los nombres de los productos del carrito (vacía si no hay)."""
        return [e.text for e in self.driver.find_elements(*self.NOMBRES)]

    def obtener_cantidad_items(self):
        return len(self.driver.find_elements(*self.ITEMS))

    def esperar_cantidad_items(self, cantidad_esperada, timeout=5):
        """
        Espera explícita a que el carrito tenga exactamente esa cantidad de
        productos. Evita leer la lista antes de que la página termine de
        actualizarse (por ej. justo después de entrar o de quitar un producto).
        """
        WebDriverWait(self.driver, timeout).until(
            lambda _: self.obtener_cantidad_items() == cantidad_esperada
        )
        return self.obtener_cantidad_items()

    def producto_esta_en_carrito(self, nombre_producto):
        return nombre_producto in self.obtener_nombres()

    def quitar_producto(self, nombre_producto):
        self.logger.info(f"Quitando del carrito: {nombre_producto}")
        self._hacer_click(self._boton_quitar(nombre_producto))

    def ir_a_checkout(self):
        self.logger.info("Iniciando checkout")
        self._hacer_click(self.BOTON_CHECKOUT)
