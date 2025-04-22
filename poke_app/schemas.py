from pydantic import BaseModel, ConfigDict, EmailStr, field_validator

from poke_app.utils import validate_type


class Message(BaseModel):
    message: str


class FilterPage(BaseModel):
    offset: int = 0
    limit: int = 20


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserList(BaseModel):
    users: list[UserResponse]


class Token(BaseModel):
    access_token: str
    token_type: str


class PokemonSchema(BaseModel):
    name: str
    type: str
    level: int = 1
    image_url: str | None = None

    @field_validator('type')
    @classmethod
    def check_type(cls, type):
        return validate_type(type)


class PokemonResponse(PokemonSchema):
    id: int
    trainer_id: int
    model_config = ConfigDict(from_attributes=True)


class PokemonList(BaseModel):
    pokemon: list[PokemonResponse]


class FilterPokemon(FilterPage):
    name: str | None = None
    type: str | None = None


class PokemonUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
