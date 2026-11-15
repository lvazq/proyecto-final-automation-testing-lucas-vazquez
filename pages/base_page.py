"""
base_page.py

Clase base de todos los Page Objects. Concentra las acciones comunes
(esperar, hacer click, escribir, leer texto) con esperas explícitas y
logging, para que las páginas concretas no repitan ese código.
"""

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from utils.logger import obtener_logger


class BasePage:
    """Acciones genéricas sobre el navegador, reutilizadas por todas las páginas."""

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.logger = obtener_logger(self.__class__.__name__)

    def _esperar_visible(self, locator):
        """Espera a que el elemento sea visible y lo devuelve."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def _hacer_click(self, locator):
        """Espera a que el elemento sea clickeable y hace click."""
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def _escribir(self, locator, texto):
        """Limpia el campo y escribe el texto indicado."""
        campo = self._esperar_visible(locator)
        campo.clear()
        if texto:
            campo.send_keys(texto)

    def _obtener_texto(self, locator):
        """Devuelve el texto visible de un elemento."""
        return self._esperar_visible(locator).text

    def _esta_visible(self, locator):
        """True si el elemento aparece visible dentro del timeout, False si no."""
        try:
            return self._esperar_visible(locator).is_displayed()
        except Exception:
            return False

    def esperar_url_contiene(self, fragmento):
        """Espera explícita a que la URL actual contenga el texto dado."""
        return self.wait.until(EC.url_contains(fragmento))

    @property
    def url_actual(self):
        return self.driver.current_url
