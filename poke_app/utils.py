from time import sleep

import requests

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon?limit=151&offset=0'
POKE_API_TYPE_URL = 'https://pokeapi.co/api/v2/type'

TEST_POKEMON_NAMES = [
    'Pikachu',
    'Bulbasaur',
    'Charmander',
    'Squirtle',
    'Eevee',
    'Snorlax',
    'Jigglypuff',
    'Gengar',
    'Meowth',
    'Mewtwo',
    'Lucario',
    'Greninja',
    'Garchomp',
    'Scizor',
    'Tyranitar',
]


def fetch_pokemon_data(url: str):
    sleep(0.3)
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
