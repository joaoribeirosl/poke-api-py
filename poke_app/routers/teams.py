from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from poke_app.auth import get_current_user
from poke_app.database import get_session
from poke_app.models import User
from poke_app.schemas import FilterPokemon, PokemonResponse, PokemonSchema

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]
Filter = Annotated[FilterPokemon, Query()]

router = APIRouter(prefix='/teams', tags=['teams'])


# Teams
# GET /times 
# POST /times
# GET /times/:id
# PUT /times/:id
# DELETE /times/:id
