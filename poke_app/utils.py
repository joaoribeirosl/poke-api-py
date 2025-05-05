from time import sleep

import requests

POKE_API_URL = 'https://pokeapi.co/api/v2/pokemon'
POKEDEX = 151


VALID_TYPES = {
    'normal',
    'fire',
    'water',
    'grass',
    'electric',
    'ice',
    'fighting',
    'poison',
    'ground',
    'flying',
    'psychic',
    'bug',
    'rock',
    'ghost',
    'dragon',
    'dark',
    'steel',
    'fairy',
}

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


def validate_type(poke_type: str) -> str:
    poke_type = poke_type.lower()
    if poke_type not in VALID_TYPES:
        raise ValueError(f"Invalid Pokemon type: '{poke_type}'")
    return poke_type


def fetch_pokemon_data(poke_id):
    sleep(0.3)
    url = f'{POKE_API_URL}/{poke_id}'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()
