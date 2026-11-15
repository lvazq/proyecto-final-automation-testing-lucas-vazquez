"""
test_jsonplaceholder.py

Pruebas de API contra JSONPlaceholder (https://jsonplaceholder.typicode.com).
Cubre GET, POST y DELETE, valida códigos de estado y estructura/contenido
del JSON, incluye un escenario de error (404) y un flujo encadenado.

Nota: JSONPlaceholder simula las escrituras (POST/DELETE responden bien
pero no persisten los datos), por eso se validan las respuestas y no el
estado posterior en el servidor.
"""

import pytest

from utils.data_reader import leer_json

pytestmark = pytest.mark.api

CAMPOS_POST = {"userId", "id", "title", "body"}
PAYLOADS_POST = leer_json("api_posts.json")


def test_get_post_existente(api):
    """GET /posts/1 -> 200 y estructura/valores esperados del JSON."""
    respuesta = api.get("/posts/1")

    assert respuesta.status_code == 200
    cuerpo = respuesta.json()
    assert CAMPOS_POST <= cuerpo.keys()
    assert cuerpo["id"] == 1
    assert isinstance(cuerpo["title"], str) and cuerpo["title"] != ""
    assert isinstance(cuerpo["userId"], int)


def test_get_listado_de_posts(api):
    """GET /posts -> 200 y una lista de 100 posts con la estructura correcta."""
    respuesta = api.get("/posts")

    assert respuesta.status_code == 200
    posts = respuesta.json()
    assert isinstance(posts, list)
    assert len(posts) == 100
    assert all(CAMPOS_POST <= post.keys() for post in posts)


def test_get_post_inexistente_devuelve_404(api):
    """ESCENARIO DE ERROR: GET de un id que no existe -> 404 y cuerpo vacío."""
    respuesta = api.get("/posts/99999")

    assert respuesta.status_code == 404
    assert respuesta.json() == {}


@pytest.mark.parametrize("caso", PAYLOADS_POST, ids=lambda caso: caso["caso"])
def test_post_crear_post(api, caso):
    """POST /posts con distintos payloads (datos/api_posts.json) -> 201 y eco del contenido."""
    payload = caso["payload"]
    respuesta = api.post("/posts", json=payload)

    assert respuesta.status_code == 201
    cuerpo = respuesta.json()
    assert cuerpo["title"] == payload["title"]
    assert cuerpo["body"] == payload["body"]
    assert cuerpo["userId"] == payload["userId"]
    assert "id" in cuerpo  # la API le asigna un id nuevo (101)


def test_delete_post(api):
    """DELETE /posts/1 -> 200 y cuerpo vacío."""
    respuesta = api.delete("/posts/1")

    assert respuesta.status_code == 200
    assert respuesta.json() == {}


def test_flujo_encadenado_usuario_y_sus_posts(api):
    """
    Peticiones encadenadas: se obtiene un usuario y, con su id, se piden
    sus posts. Se valida que todos los posts pertenezcan a ese usuario.
    """
    respuesta_usuario = api.get("/users/1")
    assert respuesta_usuario.status_code == 200
    usuario = respuesta_usuario.json()
    assert {"id", "name", "email"} <= usuario.keys()

    respuesta_posts = api.get("/posts", params={"userId": usuario["id"]})
    assert respuesta_posts.status_code == 200
    posts = respuesta_posts.json()

    assert len(posts) > 0
    assert all(post["userId"] == usuario["id"] for post in posts)
