from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from poke_app.database import get_session
from poke_app.models import PokemonType
from poke_app.schemas import (
    TypesList,
)

Session = Annotated[AsyncSession, Depends(get_session)]

router = APIRouter(prefix='/types', tags=['types'])


@router.get('/', response_model=TypesList)
async def get_all_types(session: Session):
    query = await session.scalars(select(PokemonType))
    types = query.all()
    return {'types': types}
