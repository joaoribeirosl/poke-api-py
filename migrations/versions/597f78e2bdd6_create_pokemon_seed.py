"""create pokemon seed

Revision ID: 597f78e2bdd6
Revises: 62d0b944cd96
Create Date: 2025-05-04 21:44:11.508568

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from poke_app.models import Pokemon
from poke_app.utils import POKEDEX, fetch_pokemon_data


# revision identifiers, used by Alembic.
revision: str = '597f78e2bdd6'
down_revision: Union[str, None] = '62d0b944cd96'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def pokemon_seeding():
    pokemon = []
    for poke_id in range(1, POKEDEX + 1):
        try:
            data = fetch_pokemon_data(poke_id)
            pokemon.append({
                "name": data["name"],
                "dex_no": data["id"],
                "type": data["types"][0]["type"]["name"],
                "image_url": data["sprites"]["versions"]["generation-vi"]["x-y"]["front_default"]
            })
        except Exception as e:
            print(f"Erro ao buscar pokemon {poke_id}: {e}")

    op.bulk_insert(
        Pokemon.__table__, 
        pokemon
    )

def upgrade() -> None:
    pokemon_seeding()


def downgrade() -> None:
    op.execute(sa.delete(Pokemon))