"""create types seed

Revision ID: e11982be61fc
Revises: 6a04018cef17
Create Date: 2025-05-05 15:27:35.325423

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

from poke_app.models import PokemonType
from poke_app.utils import POKE_API_TYPE_URL, fetch_pokemon_data


# revision identifiers, used by Alembic.
revision: str = 'e11982be61fc'
down_revision: Union[str, None] = '6a04018cef17'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

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


def downgrade() -> None:
    """Downgrade schema."""
    op.execute(sa.delete(PokemonType))
