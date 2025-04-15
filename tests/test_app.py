from http import HTTPStatus

from fastapi.testclient import TestClient

from poke_app.app import app


def test_right_pokemon_message():
    client = TestClient(app)
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'IPlayPokemonGoEveryDay'}
