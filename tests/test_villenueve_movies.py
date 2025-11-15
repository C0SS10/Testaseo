from testa.framework import test
import requests

BASE = "http://www.omdbapi.com/"
API_KEY = "c6915a3c"


@test("Buscar Blade Runner 2049 (Villeneuve).")
def test_search_blade_runner_2049(context):
    params = {
        "apikey": API_KEY,
        "s": "Blade Runner 2049",
        "type": "movie"
    }

    response = requests.get(BASE, params=params)
    context.assert_equal(response.status_code, 200)

    data = response.json()
    context.assert_true(any("Blade Runner 2049" in m["Title"] for m in data.get("Search", [])))


@test("Buscar Arrival (película de Villeneuve).")
def test_search_arrival(context):
    params = {
        "apikey": API_KEY,
        "s": "Arrival",
        "type": "movie"
    }
    response = requests.get(BASE, params=params)

    context.assert_equal(response.status_code, 200)
    data = response.json()

    context.assert_true(any("Arrival" in m["Title"] for m in data.get("Search", [])))
