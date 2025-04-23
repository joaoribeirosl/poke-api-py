from dataclasses import asdict

import pytest
from sqlalchemy import select

from poke_app.models import Pokemon, User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='jojo', password='testpass', email='test@test'
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == 'jojo'))

    assert asdict(user) == {
        'id': 1,
        'username': 'jojo',
        'password': 'testpass',
        'email': 'test@test',
        'created_at': time,
        'updated_at': time,
        'pokemon': [],
    }


@pytest.mark.asyncio
async def test_create_pokemon(session, user: User):
    pokemon = Pokemon(
        name='ditto',
        type='normal',
        level=52,
        image_url='test url',
        trainer_id=user.id,
    )

    session.add(pokemon)
    await session.commit()

    pokemon = await session.scalar(select(Pokemon))

    assert asdict(pokemon) == {
        'name': 'ditto',
        'id': 1,
        'type': 'normal',
        'level': 52,
        'image_url': 'test url',
        'trainer_id': 1,
    }


@pytest.mark.asyncio
async def test_user_pokemon_relationship(session, user: User):
    pokemon = Pokemon(
        name='ditto',
        type='normal',
        level=52,
        image_url='test url',
        trainer_id=user.id,
    )

    session.add(pokemon)
    await session.commit()
    await session.refresh(user)

    user = await session.scalar(select(User).where(User.id == user.id))

    assert user.pokemon == [pokemon]
