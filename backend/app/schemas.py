from pydantic import BaseModel
from typing import List, Optional

class TypeBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class AbilityBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class StatBase(BaseModel):
    id: Optional[int] = None  
    name: str
    base_stat: int
    effort: int

    class Config:
        orm_mode = True

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
    stats: List[StatBase]  

class Pokemon(PokemonBase):
    id: int
    types: List[TypeBase]
    abilities: List[AbilityBase]
    stats: List[StatBase]

    class Config:
        orm_mode = True