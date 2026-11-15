"""
conftest.py (global)

Configuración compartida por TODOS los tests (UI y API):
- Título del reporte HTML.
- Hook que, cuando un test de UI falla, guarda una captura de pantalla
  con nombre descriptivo (fecha/hora + nombre del test) y la incrusta
  en el reporte HTML.
"""

import pytest

from utils.logger import obtener_logger
from utils.screenshots import capturar_pantalla

logger = obtener_logger(__name__)


def pytest_html_report_title(report):
    """Título que aparece arriba del reporte HTML."""
    report.title = "Reporte de pruebas - Proyecto Final (UI + API)"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Se ejecuta tras cada fase de cada test (setup / call / teardown).
    Si el test falló y usa la fixture 'driver', toma el screenshot.
    """
    resultado = yield
    reporte = resultado.get_result()

    if reporte.when in ("setup", "call"):
        if reporte.failed:
            logger.error(f"FALLÓ: {item.name} ({reporte.when})")

            driver = item.funcargs.get("driver")
            if driver is not None:
                try:
                    ruta, imagen_base64 = capturar_pantalla(driver, item.name)
                    logger.error(f"Captura guardada en: {ruta}")

                    # Adjunta la captura al reporte HTML (pytest-html >= 4)
                    import pytest_html

                    extras = getattr(reporte, "extras", [])
                    extras.append(pytest_html.extras.image(imagen_base64))
                    reporte.extras = extras
                except Exception as error:
                    logger.error(f"No se pudo capturar la pantalla: {error}")
        elif reporte.passed and reporte.when == "call":
            logger.info(f"PASÓ: {item.name}")
