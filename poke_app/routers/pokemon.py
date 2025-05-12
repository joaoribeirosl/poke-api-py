from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from poke_app.database import get_session
from poke_app.models import Pokemon
from poke_app.schemas import (
    FilterPokemon,
    PokemonList,
)

Session = Annotated[AsyncSession, Depends(get_session)]
Filter = Annotated[FilterPokemon, Query()]

router = APIRouter(prefix='/pokemon', tags=['pokemon'])


@router.get('/', response_model=PokemonList)
async def get_all_pokemon(session: Session, pokemon_filter: Filter):
    query = await session.scalars(
        select(Pokemon)
        .offset(pokemon_filter.offset)
        .limit(pokemon_filter.limit)
    )

    pokemon = query.all()

    return {'pokemon': pokemon}
