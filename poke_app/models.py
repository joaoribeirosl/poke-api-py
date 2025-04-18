from datetime import datetime

from sqlalchemy import ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    pokemon: Mapped[list['Pokemon']] = relationship(
        init=False,
        cascade='all, delete-orphan',
        lazy='selectin',
    )
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )


@table_registry.mapped_as_dataclass
class Pokemon:
    __tablename__ = 'pokemon'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    name: Mapped[str]
    type: Mapped[str]
    image_url: Mapped[str] = mapped_column(nullable=True)
    trainer_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    level: Mapped[int] = mapped_column(default=1)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
