from http import HTTPStatus

from fastapi import FastAPI

from poke_app.routers import auth, pokemon, users
from poke_app.schemas import Message

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(pokemon.router)


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def pokemon():
    return {'message': 'IPlayPokemonGoEveryDay'}
