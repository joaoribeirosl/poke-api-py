from pydantic import BaseModel, ConfigDict, EmailStr


class Message(BaseModel):
    message: str


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


class PokemonResponse(BaseModel):
    id: int
    name: str
    type: str
    level: int
    image_url: str | None = None
    trainer_id: int
    model_config = ConfigDict(from_attributes=True)
