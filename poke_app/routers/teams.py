from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from poke_app.auth import get_current_user
from poke_app.database import get_session
from poke_app.models import User
from poke_app.schemas import (
    FilterPokemon,
    PokemonResponse,
    PokemonSchema,
)

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
Filter = Annotated[FilterPokemon, Query()]

router = APIRouter(prefix='/teams', tags=['teams'])


@router.post(
    '/', status_code=HTTPStatus.CREATED, response_model=PokemonResponse
)
async def insert_pokemon_to_team(
    session: Session, current_user: CurrentUser, pokemon: PokemonSchema
):
    # db_pokemon = Pokemon(
    #     name=pokemon.name,
    #     type=pokemon.type,
    #     level=pokemon.level,
    #     image_url=pokemon.image_url,
    #     trainer_id=current_user.id,
    # )
    # session.add(db_pokemon)
    # await session.commit()
    # await session.refresh(db_pokemon)
    # return db_pokemon
    pass
