"""
checkout_page.py

Page Object del proceso de checkout (datos, resumen y confirmación).
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    """Acciones y elementos del flujo de compra."""

    # Paso 1: datos del comprador
    INPUT_NOMBRE = (By.ID, "first-name")
    INPUT_APELLIDO = (By.ID, "last-name")
    INPUT_CODIGO_POSTAL = (By.ID, "postal-code")
    BOTON_CONTINUAR = (By.ID, "continue")
    MENSAJE_ERROR = (By.CSS_SELECTOR, "h3[data-test='error']")

    # Paso 2: resumen
    BOTON_FINALIZAR = (By.ID, "finish")

    # Confirmación
    TITULO_CONFIRMACION = (By.CLASS_NAME, "complete-header")

    def completar_datos(self, nombre, apellido, codigo_postal):
        """Completa el formulario del paso 1."""
        self.logger.info(f"Completando datos: '{nombre}' '{apellido}' '{codigo_postal}'")
        self._escribir(self.INPUT_NOMBRE, nombre)
        self._escribir(self.INPUT_APELLIDO, apellido)
        self._escribir(self.INPUT_CODIGO_POSTAL, codigo_postal)

    def continuar(self):
        self._hacer_click(self.BOTON_CONTINUAR)

    def obtener_mensaje_error(self):
        return self._obtener_texto(self.MENSAJE_ERROR)

    def esperar_resumen(self):
        """Espera a estar en el paso 2 (resumen de la compra)."""
        self.esperar_url_contiene("/checkout-step-two.html")

    def finalizar(self):
        self.logger.info("Finalizando la compra")
        self._hacer_click(self.BOTON_FINALIZAR)

    def obtener_mensaje_confirmacion(self):
        """Texto de confirmación mostrado al completar la compra."""
        self.esperar_url_contiene("/checkout-complete.html")
        return self._obtener_texto(self.TITULO_CONFIRMACION)

    def esta_en_paso_uno(self):
        return "/checkout-step-one.html" in self.url_actual
