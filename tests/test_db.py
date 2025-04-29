from dataclasses import asdict

import pytest
from sqlalchemy import select

from poke_app.models import Pokemon, Trainer, User


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
        'trainer': None,
    }


@pytest.mark.asyncio
async def test_create_trainer(session):
    user = User(username='blue', email='blue@pokemon.com', password='bluepass')
    session.add(user)
    await session.flush()

    trainer = Trainer(user_id=user.id)
    session.add(trainer)
    await session.commit()

    result = await session.scalar(
        select(Trainer).where(Trainer.user_id == user.id)
    )

    assert result.user_id == user.id
    assert result.user.username == 'blue'


@pytest.mark.asyncio
async def test_create_pokemon(session):
    user = User(
        username='gary', password='eevee4life', email='gary@viridian.com'
    )
    session.add(user)
    await session.flush()

    trainer = Trainer(user_id=user.id)
    session.add(trainer)
    await session.flush()

    pokemon = Pokemon(
        name='Eevee', type='Normal', trainer_id=trainer.id, image_url='url'
    )
    session.add(pokemon)
    await session.commit()

    result = await session.scalar(
        select(Pokemon).where(Pokemon.name == 'Eevee')
    )

    assert result.id == 1
    assert result.name == 'Eevee'
    assert result.type == 'Normal'
    assert result.trainer_id == trainer.id
    assert result.level == 1


@pytest.mark.asyncio
async def test_create_user_with_trainer_and_pokemon(session, mock_db_time):
    with mock_db_time(model=User) as time:
        user = User(
            username='ashketchum',
            password='pikachu123',
            email='ash@pallet.com',
        )
        session.add(user)
        await session.flush()

        trainer = Trainer(user_id=user.id)
        session.add(trainer)
        await session.flush()

        pokemon = Pokemon(
            name='Pikachu',
            type='Electric',
            trainer_id=trainer.id,
            image_url='url',
        )
        session.add(pokemon)
        await session.commit()

    db_user = await session.scalar(
        select(User).where(User.username == 'ashketchum')
    )
    db_trainer = db_user.trainer
    db_pokemon = db_trainer.pokemon[0]

    assert db_user.email == 'ash@pallet.com'
    assert db_user.trainer is not None
    assert db_user.created_at == time
    assert db_user.updated_at == time

    assert db_trainer.user_id == db_user.id
    assert db_pokemon.name == 'Pikachu'
    assert db_pokemon.trainer_id == db_trainer.id
    assert db_pokemon.type == 'Electric'


@pytest.mark.asyncio
async def test_trainer_pokemon_relationship(session, user: User):
    trainer = Trainer(user_id=user.id)
    session.add(trainer)
    await session.commit()

    expected_level = 52

    pokemon = Pokemon(
        name='ditto',
        type='normal',
        level=expected_level,
        image_url='test url',
        trainer_id=trainer.id,
    )

    session.add(pokemon)
    await session.commit()

    db_trainer = await session.scalar(
        select(Trainer).where(Trainer.user_id == user.id)
    )

    assert db_trainer.pokemon[0].name == 'ditto'
    assert db_trainer.pokemon[0].level == expected_level
    assert db_trainer.pokemon[0].trainer_id == db_trainer.id
