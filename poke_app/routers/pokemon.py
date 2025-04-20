from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from poke_app.auth import get_current_user
from poke_app.database import get_session
from poke_app.models import Pokemon, User
from poke_app.schemas import (
    FilterPokemon,
    Message,
    PokemonList,
    PokemonResponse,
    PokemonSchema,
    PokemonUpdate,
)

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
Filter = Annotated[FilterPokemon, Query()]

router = APIRouter(prefix='/pokemon', tags=['pokemon'])


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=PokemonResponse
)
async def create_pokemon(
    session: Session, current_user: CurrentUser, pokemon: PokemonSchema
):
    db_pokemon = Pokemon(
        name=pokemon.name,
        type=pokemon.type,
        level=pokemon.level,
        image_url=pokemon.image_url,
        trainer_id=current_user.id,
    )
    session.add(db_pokemon)
    await session.commit()
    await session.refresh(db_pokemon)
    return db_pokemon


@router.get('/', response_model=PokemonList)
async def get_all_pokemon_by_trainer_id(
    session: Session, current_user: CurrentUser, pokemon_filter: Filter
):
    query = select(Pokemon).where(Pokemon.trainer_id == current_user.id)

    if pokemon_filter.name:
        query = query.filter(Pokemon.name.contains(pokemon_filter.name))

    if pokemon_filter.type:
        query = query.filter(Pokemon.type.contains(pokemon_filter.type))

    pokemon = await session.scalars(
        query.offset(pokemon_filter.offset).limit(pokemon_filter.limit)
    )

    return {'pokemon': pokemon.all()}


@router.patch('/{pokemon_id}', response_model=PokemonResponse)
async def patch_pokemon(
    pokemon_id: int,
    session: Session,
    user: CurrentUser,
    pokemon: PokemonUpdate,
):
    db_pokemon = await session.scalar(
        select(Pokemon).where(
            Pokemon.trainer_id == user.id, Pokemon.id == pokemon_id
        )
    )

    if not db_pokemon:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Pokemon not found.'
        )

    for key, value in pokemon.model_dump(exclude_unset=True).items():
        setattr(db_pokemon, key, value)

    session.add(db_pokemon)
    await session.commit()
    await session.refresh(db_pokemon)

    return db_pokemon


@router.delete('/{pokemon_id}', response_model=Message)
async def delete_pokemon(
    pokemon_id: int, session: Session, current_user: CurrentUser
):
    pokemon = await session.get(Pokemon, pokemon_id)
    if not pokemon or pokemon.trainer_id != current_user.id:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail='Pokemon not found.'
        )

    await session.delete(pokemon)
    await session.commit()
    return {'message': 'Pokemon has been deleted successfully.'}
