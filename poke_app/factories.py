import random

import factory
import factory.fuzzy

from poke_app.models import Pokemon, User
from poke_app.utils import TEST_POKEMON_NAMES, VALID_TYPES


class UserFactory(factory.Factory):
    class Meta:
        model = User

    username = factory.Sequence(lambda x: f'test{x}')
    email = factory.LazyAttribute(lambda obj: f'{obj.username}@test.com')
    password = factory.LazyAttribute(lambda obj: f'{obj.username}!1')


class PokemonFactory(factory.Factory):
    class Meta:
        model = Pokemon

    name = factory.fuzzy.FuzzyChoice(TEST_POKEMON_NAMES)
    type = factory.fuzzy.FuzzyChoice(VALID_TYPES)
    level = factory.LazyAttribute(lambda _: random.randrange(1, 100))
    image_url = factory.LazyAttribute(
        lambda obj: f'https://img.pokemondb.net/sprites/x-y/normal/{obj.name.lower()}.png'
    )
