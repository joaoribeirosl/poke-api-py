import random
from http import HTTPStatus

import factory.fuzzy
import pytest

from poke_app.models import Pokemon
from poke_app.utils import TEST_POKEMON_NAMES, VALID_TYPES


def test_create_pokemon(client, token):
    response = client.post(
        '/pokemon/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'name': 'ditto',
            'type': 'normal',
            'level': 52,
            'image_url': 'test',
            'trainer_id': 1,
        },
    )
    assert response.json() == {
        'id': 1,
        'name': 'ditto',
        'type': 'normal',
        'level': 52,
        'image_url': 'test',
        'trainer_id': 1,
    }


@pytest.mark.asyncio
async def test_pokemon_list_should_return_5_pokemon(
    session, client, user, token
):
    expected_pokemon = 5
    session.add_all(
        PokemonFactory.create_batch(expected_pokemon, trainer_id=user.id)
    )
    await session.commit()

    response = client.get(
        '/pokemon/',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json().get('pokemon')) == expected_pokemon


@pytest.mark.asyncio
async def test_list_pokemon_pagination_should_return_2_pokemon(
    session, user, client, token
):
    expected_pokemon = 2
    session.add_all(PokemonFactory.create_batch(5, trainer_id=user.id))
    await session.commit()

    response = client.get(
        '/pokemon/?offset=1&limit=2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert len(response.json().get('pokemon')) == expected_pokemon


@pytest.mark.asyncio
async def test_pokemon_list_filter_name_should_return_5_pokemon(
    session, user, client, token
):
    expected_pokemon = 5
    session.add_all(
        PokemonFactory.create_batch(
            expected_pokemon, trainer_id=user.id, name='greninja'
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
    session, user, client, token
):
    expected_pokemon = 5
    session.add_all(
        PokemonFactory.create_batch(
            expected_pokemon, trainer_id=user.id, type='ghost'
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
    session, user, client, token
):
    expected_pokemon = 5
    session.add_all(
        PokemonFactory.create_batch(
            5,
            trainer_id=user.id,
            name='pikachu',
            type='electric',
        )
    )

    session.add_all(
        PokemonFactory.create_batch(
            3,
            trainer_id=user.id,
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
async def test_patch_pokemon(session, client, user, token):
    pokemon = PokemonFactory(trainer_id=user.id)

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
async def test_delete_pokemon(session, client, user, token):
    pokemon = PokemonFactory(trainer_id=user.id)

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


class PokemonFactory(factory.Factory):
    class Meta:
        model = Pokemon

    name = factory.fuzzy.FuzzyChoice(TEST_POKEMON_NAMES)
    type = factory.fuzzy.FuzzyChoice(VALID_TYPES)
    level = factory.LazyAttribute(lambda _: random.randrange(1, 100))
    image_url = factory.LazyAttribute(
        lambda obj: f'https://img.pokemondb.net/sprites/x-y/normal/{obj.name.lower()}.png'
    )

    trainer_id = 1
