from testa.framework import test
import requests
import os

BASE = "http://www.omdbapi.com/"
API_KEY = os.getenv("API_KEY_OMDB")


@test("Buscar la película 'Irreversible' de Gaspar Noé.")
def test_search_gaspar_noe_irreversible(context):
    params = {
        "apikey": API_KEY,
        "s": "Irreversible",
        "type": "movie"
    }
    response = requests.get(BASE, params=params)

    context.assert_equal(response.status_code, 200)
    data = response.json()

    context.assert_true("Search" in data, "No se encontró la clave Search")
    context.assert_true(any("Irreversible" in m["Title"] for m in data["Search"]))


@test("Buscar la película 'Love' de Gaspar Noé.")
def test_search_gaspar_noe_love(context):
    params = {
        "apikey": API_KEY,
        "s": "Love",
        "type": "movie"
    }
    response = requests.get(BASE, params=params)

    context.assert_equal(response.status_code, 200)
    data = response.json()

    context.assert_true(any("Love" in m["Title"] for m in data.get("Search", [])))