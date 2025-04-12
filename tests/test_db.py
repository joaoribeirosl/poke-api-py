from sqlalchemy import select

from poke_app.models import User


def test_create_user(session):
    new_user = User(username='jo', password='comoqsenha', email='test@test')
    session.add(new_user)
    session.commit()

    user = session.scalar(select(User).where(User.username == 'jo'))

    assert user.username == 'jo'
