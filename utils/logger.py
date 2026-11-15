"""
logger.py

Configura el logging del proyecto. Los mensajes se muestran por consola
y se guardan en reports/ejecucion.log, para poder depurar una corrida
a posteriori (qué se hizo, en qué orden y dónde falló).
"""

import logging
import os

from utils.config import CARPETA_REPORTES

RUTA_LOG = os.path.join(CARPETA_REPORTES, "ejecucion.log")


def obtener_logger(nombre):
    """
    Devuelve un logger ya configurado. Uso:

        from utils.logger import obtener_logger
        logger = obtener_logger(__name__)
        logger.info("Paso realizado")
    """
    logger = logging.getLogger(nombre)

    # Evita duplicar handlers si el logger ya fue configurado antes
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        formato = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )

        os.makedirs(CARPETA_REPORTES, exist_ok=True)
        handler_archivo = logging.FileHandler(RUTA_LOG, encoding="utf-8")
        handler_archivo.setFormatter(formato)
        logger.addHandler(handler_archivo)

        handler_consola = logging.StreamHandler()
        handler_consola.setFormatter(formato)
        logger.addHandler(handler_consola)

        # No propagar al logger raíz (evita mensajes duplicados en consola)
        logger.propagate = False

    return logger
