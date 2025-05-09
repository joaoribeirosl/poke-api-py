from http import HTTPStatus

import pytest

from poke_app.factories import PokemonFactory
from poke_app.schemas import PokemonResponse


def test_create_pokemon(client, token, trainer):
    response = client.post(
        '/pokemon/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'ditto',
            'type': 'normal',
            'level': 52,
            'image_url': 'test',
            'trainer_id': trainer.id,
        },
    )
    assert response.json() == {
        'id': 1,
        'name': 'ditto',
        'type': 'normal',
        'level': 52,
        'image_url': 'test',
        'trainer_id': trainer.id,
    }


def test_get_all_pokemon(client):
    response = client.get('/pokemon/all')
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'pokemon': []}


def test_get_pokemon_not_empty(client, pokemon):
    pokemon_schema = PokemonResponse.model_validate(pokemon).model_dump()
    response = client.get('/pokemon/all')
    assert response.json() == {'pokemon': [pokemon_schema]}


@pytest.mark.asyncio
async def test_pokemon_list_should_return_5_pokemon(
    session, client, trainer, token
):
    expected_pokemon = 5
    session.add_all(
        PokemonFactory.create_batch(expected_pokemon, trainer_id=trainer.id)
    )
    await session.commit()

    response = client.get(
        '/pokemon/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json().get('pokemon')) == expected_pokemon


@pytest.mark.asyncio
async def test_list_pokemon_pagination_should_return_2_pokemon(
    session, trainer, client, token
):
    expected_pokemon = 2
    session.add_all(PokemonFactory.create_batch(5, trainer_id=trainer.id))
    await session.commit()

    response = client.get(
        '/pokemon/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json().get('pokemon')) == expected_pokemon


@pytest.mark.asyncio
async def test_pokemon_list_filter_name_should_return_5_pokemon(
    session, trainer, client, token
):
    expected_pokemon = 5
    session.add_all(
        PokemonFactory.create_batch(
            expected_pokemon, trainer_id=trainer.id, name='greninja'
        )
    )
    await session.commit()

    response = client.get(
        '/pokemon/?name=greninja',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json().get('pokemon')) == expected_pokemon


@pytest.mark.asyncio
async def test_pokemon_list_filter_type_should_return_5_pokemon(
    session, trainer, client, token
):
    expected_pokemon = 5
    session.add_all(
        PokemonFactory.create_batch(
            expected_pokemon, trainer_id=trainer.id, type='ghost'
        )
    )
    await session.commit()

    response = client.get(
        '/pokemon/?type=ghost',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json().get('pokemon')) == expected_pokemon


@pytest.mark.asyncio
async def test_pokemon_list_filter_combined_should_return_5_pokemon(
    session, trainer, client, token
):
    expected_pokemon = 5
    session.add_all(
        PokemonFactory.create_batch(
            5,
            trainer_id=trainer.id,
            name='pikachu',
            type='electric',
        )
    )

    session.add_all(
        PokemonFactory.create_batch(
            3,
            trainer_id=trainer.id,
            name='mewtwo',
            type='psychic',
        )
    )
    await session.commit()

    response = client.get(
        '/pokemon/?name=pikachu&type=electric',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json().get('pokemon')) == expected_pokemon


def test_patch_pokemon_error(client, token):
    response = client.patch(
        '/pokemon/10',
        json={},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Pokemon not found.'}


@pytest.mark.asyncio
async def test_patch_pokemon(session, client, trainer, token):
    pokemon = PokemonFactory(trainer_id=trainer.id)

    session.add(pokemon)
    await session.commit()

    response = client.patch(
        f'/pokemon/{pokemon.id}',
        json={'name': 'lucario'},
        headers={'Authorization': f'Bearer {token}'},
    )
    assert response.status_code == HTTPStatus.OK
    assert response.json().get('name') == 'lucario'


@pytest.mark.asyncio
async def test_delete_pokemon(session, client, trainer, token):
    pokemon = PokemonFactory(trainer_id=trainer.id)

    session.add(pokemon)
    await session.commit()

    response = client.delete(
        f'/pokemon/{pokemon.id}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        'message': 'Pokemon has been deleted successfully.'
    }


def test_delete_pokemon_error(client, token):
    response = client.delete(
        f'/pokemon/{10}', headers={'Authorization': f'Bearer {token}'}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {'detail': 'Pokemon not found.'}


@pytest.mark.asyncio
async def test_trade_pokemon_success(
    session, client, trainer, other_trainer, token
):
    pokemon_user = PokemonFactory(trainer_id=trainer.id)
    pokemon_other_user = PokemonFactory(trainer_id=other_trainer.id)

    session.add_all([pokemon_user, pokemon_other_user])
    await session.commit()

    payload = {
        'offered_pokemon_id': pokemon_user.id,
        'requested_pokemon_id': pokemon_other_user.id,
    }

    response = client.post(
        '/pokemon/trade',
        headers={'Authorization': f'Bearer {token}'},
        json=payload,
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {'message': 'Trade completed successfully'}

    await session.refresh(pokemon_user)
    await session.refresh(pokemon_other_user)

    assert pokemon_user.trainer_id == other_trainer.id
    assert pokemon_other_user.trainer_id == trainer.id
