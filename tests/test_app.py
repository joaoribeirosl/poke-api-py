from http import HTTPStatus

from fastapi.testclient import TestClient

from poke_app.app import app
from poke_app.schemas import UserResponse


def test_right_pokemon_message():
    client = TestClient(app)
    response = client.get('/')

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'IPlayPokemonGoEveryDay'}


def test_create_user(client):
    response = client.post(
        '/users',
        json={
            'username': 'jo',
            'email': 'joo@coomoq.escrev',
            'password': 'test',
        },
    )
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        'username': 'jo',
        'email': 'joo@coomoq.escrev',
        'id': 1,
    }


def test_get_users(client):
    response = client.get('/users')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'users': []}


def test_get_users_not_empty(client, user):
    user_schema = UserResponse.model_validate(user).model_dump()
    response = client.get('/users/')
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'password': 'newPass',
            'username': 'joooj',
            'email': 'joo@coomoq.com',
            'id': user.id
        },
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'username': 'joooj',
        'email': 'joo@coomoq.com',
        'id': user.id,
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'User deleted'}
