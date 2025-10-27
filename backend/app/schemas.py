from pydantic import BaseModel
from typing import List, Optional

class TypeBase(BaseModel):
    name: str
    id: Optional[int] = None  # Make id optional

    class Config:
        orm_mode = True

class AbilityBase(BaseModel):
    name: str
    id: Optional[int] = None  # Make id optional

    class Config:
        orm_mode = True

class StatBase(BaseModel):
    name: str
    base_stat: int
    effort: int
    id: Optional[int] = None  # Make id optional

    class Config:
        orm_mode = True

class PokemonBase(BaseModel):
    name: str
    height: int
    weight: int
    base_experience: int
    sprite_url: str

class PokemonCreate(PokemonBase):
    types: List[str]
    abilities: List[str]
    stats: List[StatBase]

class Pokemon(PokemonBase):
    id: int
    types: List[TypeBase]
    abilities: List[AbilityBase]
    stats: List[StatBase]
    official_artwork_url: Optional[str] = ""  

    class Config:
        orm_mode = True