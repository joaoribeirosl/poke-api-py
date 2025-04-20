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
