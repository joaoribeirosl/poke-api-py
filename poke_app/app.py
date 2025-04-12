from http import HTTPStatus

from fastapi import FastAPI

from poke_app.schemas import Message, User, UserList, UserResponse

app = FastAPI()


@app.get('/', status_code=HTTPStatus.OK, response_model=Message)
def pokemon():
    return {'message': 'IPlayPokemonGoEveryDay'}


@app.post(
    '/users/', status_code=HTTPStatus.CREATED, response_model=UserResponse
)
def create_user(user: User):
    pass


@app.get('/users/', status_code=HTTPStatus.OK, response_model=UserList)
def get_users():
    pass


@app.put('/users/{user_id}', response_model=UserResponse)
def update_user(user_id: int, user: UserResponse):
    pass


@app.delete('/users/{user_id}', response_model=Message)
def delete_user(user_id: int):
    pass
