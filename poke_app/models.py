from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class Pokemon:
    __tablename__ = 'pokemon'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    dex_no: Mapped[int]
    name: Mapped[str]
    type_id: Mapped[int] = mapped_column(ForeignKey('types.id'))
    type: Mapped['PokemonType'] = relationship(
        back_populates='pokemon', init=False
    )
    image_url: Mapped[str] = mapped_column(nullable=True)


@table_registry.mapped_as_dataclass
class PokemonType:
    __tablename__ = 'types'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    name: Mapped[str]

    pokemon: Mapped[list['Pokemon']] = relationship(
        back_populates='type', init=False
    )


@table_registry.mapped_as_dataclass
class Team:
    __tablename__ = 'teams'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    name: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))


@table_registry.mapped_as_dataclass
class PokemonTeam:
    __tablename__ = 'pokemon_teams'

    id: Mapped[int] = mapped_column(
        init=False, primary_key=True, autoincrement=True
    )
    team_id: Mapped[int] = mapped_column(ForeignKey('teams.id'))
    pokemon_id: Mapped[int] = mapped_column(ForeignKey('pokemon.id'))


# class Weakness:
#     __tablename__ = 'weaknesses'

#     id: Mapped[int] = mapped_column(init=False, primary_key=True)
#     type_id: Mapped[int] = mapped_column(ForeignKey('types.id'))
#     weak_against_id: Mapped[int] = mapped_column(ForeignKey('types.id'))
#     created_at: Mapped[datetime] = mapped_column(
#         init=False, server_default=func.now()
#     )
#     updated_at: Mapped[datetime] = mapped_column(
#         init=False, server_default=func.now(), onupdate=func.now()
#     )


# class Strengthness:
#     __tablename__ = 'strengthnesses'

#     id: Mapped[int] = mapped_column(init=False, primary_key=True)
#     type_id: Mapped[int] = mapped_column(ForeignKey('types.id'))
#     strong_against_id: Mapped[int] = mapped_column(ForeignKey('types.id'))
#     created_at: Mapped[datetime] = mapped_column(
#         init=False, server_default=func.now()
#     )
#     updated_at: Mapped[datetime] = mapped_column(
#         init=False, server_default=func.now(), onupdate=func.now()
#     )


# class Ability:
#     __tablename__ = 'abilities'

#     id: Mapped[int] = mapped_column(init=False, primary_key=True)
#     name: Mapped[str]
#     description: Mapped[str]
#     power: Mapped[int]
#     accuracy: Mapped[float]
#     type_id: Mapped[int] = mapped_column(ForeignKey('types.id'))
#     created_at: Mapped[datetime] = mapped_column(
#         init=False, server_default=func.now()
#     )
#     updated_at: Mapped[datetime] = mapped_column(
#         init=False, server_default=func.now(), onupdate=func.now()
#     )


# class PokemonAbility:
#     __tablename__ = 'pokemon_abilities'

#     id: Mapped[int] = mapped_column(init=False, primary_key=True)
#     pokemon_id: Mapped[int] = mapped_column(ForeignKey('pokemon.id'))
#     ability_id: Mapped[int] = mapped_column(ForeignKey('abilities.id'))
#     created_at: Mapped[datetime] = mapped_column(
#         init=False, server_default=func.now()
#     )
#     updated_at: Mapped[datetime] = mapped_column(
#         init=False, server_default=func.now(), onupdate=func.now()
#     )
