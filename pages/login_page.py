"""
login_page.py

Page Object de la página de login de saucedemo.com.
"""

from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from utils.config import URL_BASE_UI


class LoginPage(BasePage):
    """Acciones y elementos de la pantalla de login."""

    INPUT_USUARIO = (By.ID, "user-name")
    INPUT_PASSWORD = (By.ID, "password")
    BOTON_LOGIN = (By.ID, "login-button")
    MENSAJE_ERROR = (By.CSS_SELECTOR, "h3[data-test='error']")

    def abrir(self):
        """Navega a la página de login."""
        self.logger.info(f"Abriendo {URL_BASE_UI}")
        self.driver.get(URL_BASE_UI)
        return self

    def login(self, usuario, password):
        """Completa usuario y contraseña y presiona el botón de login."""
        self.logger.info(f"Login con usuario '{usuario}'")
        self._escribir(self.INPUT_USUARIO, usuario)
        self._escribir(self.INPUT_PASSWORD, password)
        self._hacer_click(self.BOTON_LOGIN)

    def esperar_inventario(self):
        """Espera explícita a la redirección a /inventory.html."""
        self.esperar_url_contiene("/inventory.html")

    def obtener_mensaje_error(self):
        """Devuelve el texto del mensaje de error mostrado en el login."""
        return self._obtener_texto(self.MENSAJE_ERROR)

    def esta_en_login(self):
        """True si seguimos en la página de login (no hubo redirección)."""
        return "/inventory.html" not in self.url_actual and self._esta_visible(self.BOTON_LOGIN)
