from pydantic import BaseModel
from typing import List, Optional

class TypeBase(BaseModel):
    name: str

class TypeCreate(TypeBase):
    pass

class Type(TypeBase):
    id: int

    class Config:
        from_attributes = True

class AbilityBase(BaseModel):
    name: str

class AbilityCreate(AbilityBase):
    pass

class Ability(AbilityBase):
    id: int

    class Config:
        from_attributes = True

class StatBase(BaseModel):
    name: str
    base_stat: int
    effort: int

class StatCreate(StatBase):
    pass

class Stat(StatBase):
    id: int

    class Config:
        from_attributes = True

class PokemonBase(BaseModel):
    name: str
    height: int
    weight: int
    base_experience: int
    sprite_url: str
    official_artwork_url: str

class PokemonCreate(PokemonBase):
    types: List[str]
    abilities: List[str]
    stats: List[StatCreate]

class Pokemon(PokemonBase):
    id: int
    types: List[Type]
    abilities: List[Ability]
    stats: List[Stat]

    class Config:
        from_attributes = True

class PokemonList(BaseModel):
    pokemon: List[Pokemon]
    total: int