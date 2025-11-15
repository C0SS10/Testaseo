# 🌟 Testa — Un framework minimalista y hermoso para testing en Python

![Python Badge](https://img.shields.io/badge/Python-3.13-blue.svg)
![Poetry Badge](https://img.shields.io/badge/Poetry-Dependency_Management-60A5FA.svg)
![License Badge](https://img.shields.io/badge/License-MIT-green.svg)

> *Simple y Poderoso.*  
> Testa es un micro-framework para ejecutar tests de funcionalidades (APIs u otras) con salida en consola bonita, diffs inteligentes y ejecución paralela con hilos.

---

### >[!IMPORTANT]
> Usa **Poetry** para gestionar el entorno. Si no lo tienes:
>
> ```bash
> pip install poetry
> ```

---

## 📁 Estructura recomendada

```bash
.
├── testa/
│ ├── framework.py
│ ├── runner.py
│ ├── models/
│ │ ├── test_context.py
│ │ ├── test_result.py
│ │ └── colors.py
│ └── exceptions/
│ └── assertion_error_detailed.py
├── tests/
│ ├── test_a24_movies.py
│ ├── test_gaspar_noe_movies.py
│ └── test_failures.py
├── main.py
├── pyproject.toml
└── README.md
```
---

## 🚀 Instalación (Poetry)

```bash
poetry install
```

>[!IMPORTANT]
> Si requests no está disponible, asegúrate de correr dentro del entorno creado por Poetry: Iniciar con Poetry: poetry run python main.py O activar venv manual (Windows): .\.venv\Scripts\activate

## ▶️ Ejecutar tests

Ejecuta todos los tests (autodiscovery incluido):

```bash
poetry run python main.py
```

### ✍️ Cómo escribir tests

Cada test es una función decorada con @test o @test("Descripción").

La función recibe un solo argumento context (TestContext).

Ejemplo: `tests/test_a24_movies.py`

```python
from testa.framework import test
import requests

BASE = "http://www.omdbapi.com/"
API_KEY = "YOUR_API_KEY"

@test("Buscar 'Hereditary' (A24).")
def test_search_a24_hereditary(context):
    params = {"apikey": API_KEY, "s": "Hereditary", "type": "movie"}
    response = requests.get(BASE, params=params)
    context.assert_equal(response.status_code, 200)
    data = response.json()
    context.assert_true(any("Hereditary" in m["Title"] for m in data.get("Search", [])))
```