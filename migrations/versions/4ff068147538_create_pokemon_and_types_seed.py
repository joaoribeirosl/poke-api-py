"""create pokemon and types seed

Revision ID: 4ff068147538
Revises: 40c0222b8c15
Create Date: 2025-05-06 12:01:56.112193

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from poke_app.models import Pokemon, PokemonType
from poke_app.utils import POKE_API_TYPE_URL, POKE_API_URL, fetch_pokemon_data


# revision identifiers, used by Alembic.
revision: str = '4ff068147538'
down_revision: Union[str, None] = '40c0222b8c15'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def types_seeding():
    type_list = []
    data = fetch_pokemon_data(POKE_API_TYPE_URL)["results"]
    for pokemon_type in data:
        type_list.append({
            "name": pokemon_type["name"]
        })

    op.bulk_insert(
        PokemonType.__table__, 
        type_list
    )


def pokemon_seeding():

    connection = op.get_bind()
    result = connection.execute(sa.select(PokemonType.id, PokemonType.name))
    type_mapping = {row.name: row.id for row in result}

    pokemon = []
    data = fetch_pokemon_data(POKE_API_URL)["results"]
    for pokemon_data in data:
        response = fetch_pokemon_data(pokemon_data["url"])
        primary_type_name = response["types"][0]["type"]["name"]
        type_id = type_mapping.get(primary_type_name)
        pokemon.append({
                "name": pokemon_data["name"],
                "dex_no": response["id"],
                "type_id": type_id,
                "image_url": response["sprites"]["versions"]["generation-vi"]["x-y"]["front_default"]
            })

    op.bulk_insert(
        Pokemon.__table__, 
        pokemon
    )

def upgrade() -> None:
    types_seeding()
    pokemon_seeding()


def downgrade() -> None:
    op.execute(sa.delete(PokemonType))
    op.execute(sa.delete(Pokemon))
