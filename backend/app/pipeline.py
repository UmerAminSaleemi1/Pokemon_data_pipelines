import requests
import logging
from sqlalchemy.orm import Session
from . import models, schemas
from .config import settings

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PokemonPipeline:
    def __init__(self):
        self.base_url = settings.POKEAPI_BASE_URL
#Fetch raw Pokemon data from PokemonAPI
    def fetch_pokemon_data(self, pokemon_id: int) -> dict:
        
        try:
            response = requests.get(f"{self.base_url}/pokemon/{pokemon_id}")
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Error fetching Pokémon {pokemon_id}: {e}")
            return None
#Transforming raw API data into structured format
    def transform_pokemon_data(self, raw_data: dict) -> schemas.PokemonCreate:
    
        
        # Extract sprites
        sprites = raw_data.get('sprites', {})
        sprite_url = sprites.get('front_default', '')
        official_artwork = sprites.get('other', {}).get('official-artwork', {}).get('front_default', '')

        # Extract types
        types = [type_data['type']['name'] for type_data in raw_data.get('types', [])]

        # Extract abilities
        abilities = [ability_data['ability']['name'] for ability_data in raw_data.get('abilities', [])]

        # Extract stats
        stats = []
        for stat_data in raw_data.get('stats', []):
            stats.append(schemas.StatBase(
                name=stat_data['stat']['name'],
                base_stat=stat_data['base_stat'],
                effort=stat_data['effort']
            ))

        return schemas.PokemonCreate(
            name=raw_data['name'],
            height=raw_data['height'],
            weight=raw_data['weight'],
            base_experience=raw_data.get('base_experience', 0),
            sprite_url=sprite_url,
            official_artwork_url=official_artwork,
            types=types,
            abilities=abilities,
            stats=stats
        )
#Get existing type or create new one
    def get_or_create_type(self, db: Session, type_name: str) -> models.Type:
        
        db_type = db.query(models.Type).filter(models.Type.name == type_name).first()
        if not db_type:
            db_type = models.Type(name=type_name)
            db.add(db_type)
            db.commit()
            db.refresh(db_type)
        return db_type
#Get existing ability or create new one
    def get_or_create_ability(self, db: Session, ability_name: str) -> models.Ability:
        
        db_ability = db.query(models.Ability).filter(models.Ability.name == ability_name).first()
        if not db_ability:
            db_ability = models.Ability(name=ability_name)
            db.add(db_ability)
            db.commit()
            db.refresh(db_ability)
        return db_ability
#Load transformed Pokemon data into PostgreSQL database
    def load_pokemon_data(self, db: Session, pokemon_data: schemas.PokemonCreate) -> models.Pokemon:
        
        # Check if Pokemon already exists
        existing_pokemon = db.query(models.Pokemon).filter(models.Pokemon.name == pokemon_data.name).first()
        if existing_pokemon:
            logger.info(f"Pokémon {pokemon_data.name} already exists, skipping...")
            return existing_pokemon

        # Create Pokemon
        db_pokemon = models.Pokemon(
            name=pokemon_data.name,
            height=pokemon_data.height,
            weight=pokemon_data.weight,
            base_experience=pokemon_data.base_experience,
            sprite_url=pokemon_data.sprite_url,
            official_artwork_url=pokemon_data.official_artwork_url
        )
        db.add(db_pokemon)
        db.commit()
        db.refresh(db_pokemon)

        # Add types
        for type_name in pokemon_data.types:
            db_type = self.get_or_create_type(db, type_name)
            db_pokemon.types.append(db_type)

        # Add abilities
        for ability_name in pokemon_data.abilities:
            db_ability = self.get_or_create_ability(db, ability_name)
            db_pokemon.abilities.append(db_ability)

        # Add stats
        for stat_data in pokemon_data.stats:
            db_stat = models.Stat(
                name=stat_data.name,
                base_stat=stat_data.base_stat,
                effort=stat_data.effort,
                pokemon_id=db_pokemon.id
            )
            db.add(db_stat)

        db.commit()
        db.refresh(db_pokemon)
        logger.info(f"Successfully loaded Pokémon: {pokemon_data.name}")
        return db_pokemon
#Run the complete ETL pipeline for a range of Pokemon
    def run_pipeline(self, db: Session, start_id: int = 1, end_id: int = 20):
        
        logger.info(f"Starting Pokémon pipeline for IDs {start_id} to {end_id}")
        
        successful = 0
        failed = 0

        for pokemon_id in range(start_id, end_id + 1):
            try:
                # Extract
                raw_data = self.fetch_pokemon_data(pokemon_id)
                if not raw_data:
                    failed += 1
                    continue

                # Transform
                transformed_data = self.transform_pokemon_data(raw_data)

                # Load
                self.load_pokemon_data(db, transformed_data)
                successful += 1

            except Exception as e:
                logger.error(f"Error processing Pokémon {pokemon_id}: {e}")
                failed += 1

        logger.info(f"Pipeline completed. Successful: {successful}, Failed: {failed}")
        return {"successful": successful, "failed": failed}