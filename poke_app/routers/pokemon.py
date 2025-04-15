from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from poke_app.auth import get_current_user
from poke_app.database import get_session
from poke_app.models import User

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/pokemon', tags=['pokemon'])
