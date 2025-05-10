from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from poke_app.auth import get_current_user
from poke_app.database import get_session
from poke_app.models import PokemonTeam, Team, User
from poke_app.schemas import TeamCreate, TeamList, TeamResponse

Session = Annotated[AsyncSession, Depends(get_session)]
CurrentUser = Annotated[User, Depends(get_current_user)]

router = APIRouter(prefix='/teams', tags=['teams'])


@router.get('/', response_model=TeamList)
async def get_user_teams(session: Session, user: CurrentUser):
    result = await session.execute(select(Team).where(Team.user_id == user.id))
    teams = result.scalars().all()

    team_list = []

    for team in teams:
        result = await session.execute(
            select(PokemonTeam.pokemon_id).where(
                PokemonTeam.team_id == team.id
            )
        )
        pokemon_ids = [row[0] for row in result.all()]

        team_list.append(
            TeamResponse(id=team.id, name=team.name, pokemon_ids=pokemon_ids)
        )

    return {'teams': team_list}


@router.post('/', response_model=TeamResponse)
async def create_team(data: TeamCreate, session: Session, user: CurrentUser):
    team = Team(user_id=user.id, name=data.name)
    session.add(team)
    await session.flush()

    for poke_id in data.pokemon_ids:
        pokemon_team_db = PokemonTeam(team_id=team.id, pokemon_id=poke_id)
        session.add(pokemon_team_db)

    await session.commit()
    team_response = TeamResponse(
        id=team.id, name=team.name, pokemon_ids=data.pokemon_ids
    )

    return team_response
