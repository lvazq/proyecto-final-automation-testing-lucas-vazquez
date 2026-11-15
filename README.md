# Proyecto Final – Automatización de Testing (UI + API)

## Propósito del proyecto

Suite de pruebas automatizadas que combina:

- **Pruebas de UI** sobre [saucedemo.com](https://www.saucedemo.com/) con
  Selenium WebDriver y el patrón **Page Object Model (POM)**.
- **Pruebas de API** sobre [JSONPlaceholder](https://jsonplaceholder.typicode.com/)
  con la librería `requests`.

Incluye datos de prueba externos (CSV/JSON), capturas de pantalla
automáticas en los fallos, logging, reporte HTML y ejecución
automática en **GitHub Actions** en cada push.

## Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python 3.9+ | Lenguaje principal |
| Pytest | Estructura, parametrización y ejecución de los tests |
| Selenium WebDriver | Automatización del navegador (UI) |
| webdriver-manager | Descarga automática del ChromeDriver correcto |
| Requests | Pruebas de API |
| pytest-html | Reporte HTML de resultados |
| GitHub Actions | Integración continua (CI) |
| Git / GitHub | Control de versiones |

## Estructura del proyecto

```
proyecto_final/
├── .github/workflows/
│   └── tests.yml            # Pipeline de CI (GitHub Actions)
├── pages/                   # Page Objects (UI)
│   ├── base_page.py         # Acciones comunes con esperas explícitas
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   └── checkout_page.py
├── tests/
│   ├── conftest.py          # Hook de capturas en fallos + título del reporte
│   ├── ui/
│   │   ├── conftest.py      # Fixtures: driver y sesión iniciada
│   │   ├── test_login.py
│   │   ├── test_inventory.py
│   │   ├── test_cart.py
│   │   └── test_checkout.py
│   └── api/
│       ├── conftest.py      # Fixture: cliente HTTP
│       └── test_jsonplaceholder.py
├── utils/                   # Funciones auxiliares
│   ├── config.py            # URLs, credenciales y rutas
│   ├── driver_factory.py    # Creación del driver (Service + webdriver-manager)
│   ├── data_reader.py       # Lectura de CSV / JSON
│   ├── screenshots.py       # Captura de pantalla con fecha/hora y nombre del test
│   ├── logger.py            # Configuración del logging
│   └── api_client.py        # Cliente HTTP con logging
├── datos/                   # Datos de prueba externos
│   ├── login.csv
│   ├── productos.json
│   ├── checkout.json
│   └── api_posts.json
├── reports/                 # Reporte HTML, log y capturas (se generan al ejecutar)
├── pytest.ini               # Configuración de pytest (reporte HTML, marcadores)
├── requirements.txt
└── README.md
```

### Cómo se aplica el POM

Toda la interacción con el navegador (locators, clicks, esperas) vive en
`pages/`. Los tests en `tests/ui/` solo llaman a métodos como
`login.login(...)` o `inventario.agregar_producto(...)` y hacen las
aserciones: si el HTML del sitio cambia, se corrige un locator en una
página y no en cada test.

## Casos de prueba

### UI (saucedemo.com)

| Archivo | Qué valida |
|---|---|
| `test_login.py` | Login parametrizado con `datos/login.csv`: caso válido y **negativos** (usuario bloqueado, contraseña incorrecta, usuario inexistente, campos vacíos) |
| `test_inventory.py` | Título, 6 productos visibles, menú/filtro/carrito presentes, nombre y precio del primer producto, ordenamiento por precio |
| `test_cart.py` | Agregar cada producto de `datos/productos.json`, contador del carrito, contenido del carrito, agregar varios, quitar un producto |
| `test_checkout.py` | Compra completa de punta a punta + **negativos**: formulario sin nombre / apellido / código postal (`datos/checkout.json`) |

### API (JSONPlaceholder)

| Test | Método | Qué valida |
|---|---|---|
| `test_get_post_existente` | GET | Status 200 y estructura/tipos del JSON |
| `test_get_listado_de_posts` | GET | Lista de 100 posts con los campos esperados |
| `test_get_post_inexistente_devuelve_404` | GET | Escenario de error (404) |
| `test_post_crear_post` | POST | Status 201 y eco del contenido (3 payloads de `datos/api_posts.json`) |
| `test_delete_post` | DELETE | Status 200 y cuerpo vacío |
| `test_flujo_encadenado_usuario_y_sus_posts` | GET → GET | La respuesta de la 1.ª petición alimenta la 2.ª |

> JSONPlaceholder simula las escrituras: POST/DELETE responden correctamente
> pero no persisten datos. Por eso se valida la respuesta, no el estado posterior.

## Instalación de dependencias

Requisitos previos: **Python 3.9+** y **Google Chrome** instalado.

```bash
# 1. Crear y activar un entorno virtual (recomendado)
python3 -m venv venv
source venv/bin/activate        # En Windows: venv\Scripts\activate

# 2. Instalar dependencias
python3 -m pip install -r requirements.txt
```

## Cómo ejecutar las pruebas

La configuración de `pytest.ini` ya incluye el reporte HTML, así que alcanza con:

```bash
python3 -m pytest
```

Otras variantes útiles:

```bash
python3 -m pytest -m ui                      # solo pruebas de UI
python3 -m pytest -m api                     # solo pruebas de API
python3 -m pytest tests/ui/test_login.py     # un solo archivo
HEADLESS=true python3 -m pytest              # UI sin abrir ventana de Chrome
```

## Cómo interpretar los reportes generados

Cada ejecución genera tres evidencias en `reports/`:

1. **`reporte.html`** – abrilo con el navegador. Muestra:
   - un resumen arriba (cantidad de tests pasados, fallados, errores);
   - una tabla con cada test, su **resultado** (Passed / Failed / Error),
     su **duración** y, al expandir la fila, el detalle del error y el log;
   - en los tests de UI que fallaron, la **captura de pantalla** del
     navegador en el momento del fallo.
2. **`screenshots/`** – las capturas como archivos PNG, con nombres tipo
   `20261115_183045_test_login_usuario_bloqueado.png` (fecha, hora y nombre
   del test).
3. **`ejecucion.log`** – registro paso a paso (navegación, login, clicks,
   peticiones HTTP con su status y tiempo, resultado de cada test). Es el
   primer lugar donde mirar para depurar un fallo.

## Integración continua (GitHub Actions)

El workflow `.github/workflows/tests.yml` se dispara en cada **push** y
en cada pull request hacia `main`. Instala las dependencias, ejecuta toda
la suite en modo headless y sube la carpeta `reports/` como **artefacto**
(incluso si hay tests fallidos).

Para ver los reportes: pestaña **Actions** del repo → seleccionar la
ejecución → sección **Artifacts** → descargar `reportes-pytest`.

## Flujo de trabajo con Git

Se desarrolla con ramas por funcionalidad que luego se fusionan a `main`:

```bash
git checkout -b feature/api-tests      # crear rama
# ...cambios...
git add .
git commit -m "Agrega tests de API con JSONPlaceholder"
git checkout main
git merge feature/api-tests            # fusionar a main
git push
```
