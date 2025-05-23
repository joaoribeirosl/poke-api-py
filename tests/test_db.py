from dataclasses import asdict

import pytest
from sqlalchemy import select

from poke_app.models import User


@pytest.mark.asyncio
async def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(
            username='jojo', password='testpass', email='test@test'
        )
        session.add(new_user)
        await session.commit()

    user = await session.scalar(select(User).where(User.username == 'jojo'))

    assert asdict(user) == {
        'id': 1,
        'username': 'jojo',
        'password': 'testpass',
        'email': 'test@test',
        'created_at': time,
        'updated_at': time,
    }

