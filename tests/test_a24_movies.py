from testa.framework import test
import requests

BASE = "http://www.omdbapi.com/"
API_KEY = "c6915a3c"


@test("Buscar 'Hereditary' (A24).")
def test_search_a24_hereditary(context):
    params = {
        "apikey": API_KEY,
        "s": "Hereditary",
        "type": "movie"
    }

    response = requests.get(BASE, params=params)
    context.assert_equal(response.status_code, 200)

    data = response.json()
    context.assert_true(any("Hereditary" in m["Title"] for m in data.get("Search", [])))

@test("Buscar 'Midsommar' (A24).")
def test_search_a24_midsommar(context):
    params = {
        "apikey": API_KEY,
        "s": "Midsommar",
        "type": "movie"
    }

    response = requests.get(BASE, params=params)
    context.assert_equal(response.status_code, 200)

    data = response.json()
    context.assert_true(any("Midsommar" in m["Title"] for m in data.get("Search", [])))