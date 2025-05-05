from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from poke_app.auth import get_current_user
from poke_app.database import get_session
from poke_app.models import Pokemon, User
from poke_app.schemas import (
    FilterPokemon,
    PokemonList,
)

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
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


# @router.get('/id', response_model=PokemonList)
# async def get_all_pokemon_by_trainer_id(
#     session: Session, current_user: CurrentUser, pokemon_filter: Filter
# ):
#     query = select(Pokemon).where(Pokemon.trainer_id == current_user.id)

#     if pokemon_filter.name:
#         query = query.filter(Pokemon.name.contains(pokemon_filter.name))

#     if pokemon_filter.type:
#         query = query.filter(Pokemon.type.contains(pokemon_filter.type))

#     pokemon = await session.scalars(
#         query.offset(pokemon_filter.offset).limit(pokemon_filter.limit)
#     )

#     return {'pokemon': pokemon.all()}


# @router.patch('/{pokemon_id}', response_model=PokemonResponse)
# async def patch_pokemon(
#     pokemon_id: int,
#     session: Session,
#     user: CurrentUser,
#     pokemon: PokemonUpdate,
# ):
#     db_pokemon = await session.scalar(
#         select(Pokemon).where(
#             Pokemon.trainer_id == user.id, Pokemon.id == pokemon_id
#         )
#     )

#     if not db_pokemon:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND, detail='Pokemon not found.'
#         )

#     for key, value in pokemon.model_dump(exclude_unset=True).items():
#         setattr(db_pokemon, key, value)

#     session.add(db_pokemon)
#     await session.commit()
#     await session.refresh(db_pokemon)

#     return db_pokemon


# @router.delete('/{pokemon_id}', response_model=Message)
# async def delete_pokemon(
#     pokemon_id: int, session: Session, current_user: CurrentUser
# ):
#     pokemon = await session.get(Pokemon, pokemon_id)
#     if not pokemon or pokemon.trainer_id != current_user.id:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND, detail='Pokemon not found.'
#         )

#     await session.delete(pokemon)
#     await session.commit()
#     return {'message': 'Pokemon has been deleted successfully.'}


# @router.post('/trade', response_model=Message)
# async def trade_pokemon(
#     trade: TradeRequest,
#     session: Session,
#     current_user: CurrentUser,
# ):
#     offered_pokemon = await session.scalar(
#         select(Pokemon).where(Pokemon.id == trade.offered_pokemon_id)
#     )

#     if not offered_pokemon:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND,
#             detail='Offered Pokemon not found',
#         )

#     if offered_pokemon.trainer_id != current_user.id:
#         raise HTTPException(
#             status_code=HTTPStatus.FORBIDDEN,
#             detail="You don't own the offered Pokémon",
#         )

#     requested_pokemon = await session.scalar(
#         select(Pokemon).where(Pokemon.id == trade.requested_pokemon_id)
#     )

#     if not requested_pokemon:
#         raise HTTPException(
#             status_code=HTTPStatus.NOT_FOUND,
#             detail='Requested Pokémon not found',
#         )

#     if requested_pokemon.trainer_id == current_user.id:
#         raise HTTPException(
#             status_code=HTTPStatus.BAD_REQUEST,
#             detail='You already own the requested Pokémon',
#         )

#     offered_pokemon.trainer_id, requested_pokemon.trainer_id = (
#         requested_pokemon.trainer_id,
#         offered_pokemon.trainer_id,
#     )
#     await session.commit()

#     return {'message': 'Trade completed successfully'}
