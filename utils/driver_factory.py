"""
driver_factory.py

Crea y configura el WebDriver de Chrome.

- Service + webdriver-manager: descarga y gestiona automáticamente el
  ChromeDriver compatible con la versión de Chrome instalada.
- Modo headless: se activa con la variable de entorno HEADLESS=true
  (así lo usa GitHub Actions, que no tiene pantalla).
"""

import os

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def crear_driver(headless=None):
    """
    Devuelve una instancia de Chrome lista para usar.

    headless: True/False para forzarlo. Si es None, se decide según la
    variable de entorno HEADLESS (por defecto, con ventana visible).
    """
    if headless is None:
        headless = os.getenv("HEADLESS", "false").lower() == "true"

    opciones = webdriver.ChromeOptions()
    opciones.add_argument("--disable-notifications")
    opciones.add_argument("--window-size=1920,1080")

    # Desactiva el gestor de contraseñas de Chrome: sin esto, aparece un
    # popup ("cambiá tu contraseña") que puede tapar elementos en saucedemo.
    opciones.add_experimental_option(
        "prefs",
        {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        },
    )

    if headless:
        opciones.add_argument("--headless=new")
        # Argumentos necesarios para correr estable en servidores de CI
        opciones.add_argument("--no-sandbox")
        opciones.add_argument("--disable-dev-shm-usage")

    servicio = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=servicio, options=opciones)
