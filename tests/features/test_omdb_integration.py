import os
import requests
from testa.framework import test


BASE = "http://www.omdbapi.com/"
API_KEY = os.getenv("API_KEY_OMDB")


@test("Debe obtener información de una película real desde OMDB", category="integration")
def test_omdb_search(context):
    assert API_KEY is not None, "API_KEY_OMDB no está definida en el .env"

    params = {
        "t": "Inception",
        "apikey": API_KEY
    }

    response = requests.get(BASE, params=params)
    data = response.json()

    assert response.status_code == 200
    assert data["Response"] == "True"
    assert data["Title"] == "Inception"


@test("Debe retornar error para una película inexistente", category="integration")
def test_omdb_not_found(context):
    params = {
        "t": "askjfjaskjd", 
        "apikey": API_KEY
    }

    response = requests.get(BASE, params=params)
    data = response.json()

    assert response.status_code == 200
    assert data["Response"] == "False"
    assert "Error" in data
