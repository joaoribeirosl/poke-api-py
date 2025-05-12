from http import HTTPStatus


def test_get_all_pokemon(client):
    response = client.get('/pokemon')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'pokemon': []}
