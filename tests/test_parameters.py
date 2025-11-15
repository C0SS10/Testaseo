from testa.framework import test
import requests
import os

BASE = "http://www.omdbapi.com/"
API_KEY = os.getenv("API_KEY_OMDB")


@test("Si no se envía 's', OMDb debe devolver error.")
def test_invalid_search_returns_error(context):
    params = {"apikey": API_KEY}
    response = requests.get(BASE, params=params)

    context.assert_equal(response.status_code, 200)
    data = response.json()

    context.assert_true("Error" in data)

@test("Probar paginación con la búsqueda 'Batman'.")
def test_page_parameter(context):
    params = {
        "apikey": API_KEY,
        "s": "Batman",
        "page": 2
    }

    response = requests.get(BASE, params=params)
    context.assert_equal(response.status_code, 200)

    data = response.json()
    context.assert_true("Search" in data)


@test("Buscar solo series con 'The Office'.")
def test_type_filter_series(context):
    params = {
        "apikey": API_KEY,
        "s": "The Office",
        "type": "series"
    }

    response = requests.get(BASE, params=params)
    context.assert_equal(response.status_code, 200)
    data = response.json()

    for item in data.get("Search", []):
        context.assert_equal(item["Type"], "series")


@test("Probar respuesta en formato XML.")
def test_output_xml(context):
    params = {
        "apikey": API_KEY,
        "s": "Batman",
        "r": "xml"
    }

    response = requests.get(BASE, params=params)
    context.assert_equal(response.status_code, 200)

    # Validación básica: XML empieza con '<'
    context.assert_true(response.text.strip().startswith("<"))
