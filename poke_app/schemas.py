from pydantic import BaseModel, ConfigDict, EmailStr


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
    dex_no: int
    name: str
    type_id: int
    image_url: str | None = None


class PokemonResponse(PokemonSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PokemonList(BaseModel):
    pokemon: list[PokemonResponse]


class FilterPokemon(FilterPage):
    name: str | None = None
    type: str | None = None


class PokemonUpdate(BaseModel):
    name: str | None = None
    type: str | None = None


class TradeRequest(BaseModel):
    offered_pokemon_id: int
    requested_pokemon_id: int
