from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

# Association tables for many-to-many relationships
pokemon_types = Table(
    'pokemon_types',
    Base.metadata,
    Column('pokemon_id', Integer, ForeignKey('pokemon.id')),
    Column('type_id', Integer, ForeignKey('types.id'))
)

pokemon_abilities = Table(
    'pokemon_abilities',
    Base.metadata,
    Column('pokemon_id', Integer, ForeignKey('pokemon.id')),
    Column('ability_id', Integer, ForeignKey('abilities.id'))
)

class Pokemon(Base):
    __tablename__ = "pokemon"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    height = Column(Integer)
    weight = Column(Integer)
    base_experience = Column(Integer)
    sprite_url = Column(String)
    official_artwork_url = Column(String)

    # Relationships
    types = relationship("Type", secondary=pokemon_types, back_populates="pokemon")
    abilities = relationship("Ability", secondary=pokemon_abilities, back_populates="pokemon")
    stats = relationship("Stat", back_populates="pokemon")

class Type(Base):
    __tablename__ = "types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    pokemon = relationship("Pokemon", secondary=pokemon_types, back_populates="types")

class Ability(Base):
    __tablename__ = "abilities"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    pokemon = relationship("Pokemon", secondary=pokemon_abilities, back_populates="abilities")

class Stat(Base):
    __tablename__ = "stats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    base_stat = Column(Integer)
    effort = Column(Integer)
    pokemon_id = Column(Integer, ForeignKey('pokemon.id'))

    pokemon = relationship("Pokemon", back_populates="stats")