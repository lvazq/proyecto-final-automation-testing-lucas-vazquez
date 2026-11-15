"""
config.py

Constantes de configuración centralizadas: URLs base y credenciales del
usuario válido de práctica. Así, si algo cambia, se corrige en un solo lugar.
"""

import os

# Raíz del proyecto (carpeta que contiene utils/, pages/, tests/, etc.)
RAIZ_PROYECTO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# --- UI (saucedemo.com) ---
URL_BASE_UI = "https://www.saucedemo.com/"
USUARIO_VALIDO = "standard_user"
PASSWORD_VALIDO = "secret_sauce"

# --- API (JSONPlaceholder) ---
URL_BASE_API = "https://jsonplaceholder.typicode.com"

# --- Carpetas de salida ---
CARPETA_DATOS = os.path.join(RAIZ_PROYECTO, "datos")
CARPETA_REPORTES = os.path.join(RAIZ_PROYECTO, "reports")
CARPETA_CAPTURAS = os.path.join(CARPETA_REPORTES, "screenshots")
