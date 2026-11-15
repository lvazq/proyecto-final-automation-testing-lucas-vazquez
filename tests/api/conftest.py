"""
conftest.py (API)

Fixture que entrega un cliente HTTP listo para usar en los tests de API.
"""

import pytest

from utils.api_client import ApiClient


@pytest.fixture(scope="module")
def api():
    """Cliente de JSONPlaceholder compartido por los tests de cada módulo."""
    return ApiClient()
