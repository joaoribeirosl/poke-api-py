from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def pokemon():
    return {'message': 'IPlayPokemonGoEveryDay'}
