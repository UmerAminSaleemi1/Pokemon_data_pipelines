from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, pipeline
from .database import engine, get_db

# Creating database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pokemon Data Pipeline", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initializing pipeline
pokemon_pipeline = pipeline.PokemonPipeline()

@app.post("/pokemon/run-pipeline/")
def run_pipeline(
    start_id: int = 1,
    end_id: int = 20,
    db: Session = Depends(get_db)
):
    #Trigger the ETL pipeline
    result = pokemon_pipeline.run_pipeline(db, start_id, end_id)
    return result

@app.get("/pokemon/", response_model=List[schemas.Pokemon])
def get_pokemon(
    skip: int = 0,
    limit: int = 20,
    type_filter: str = None,
    db: Session = Depends(get_db)
):
    #Get all Pokemon with optional filtering
    query = db.query(models.Pokemon)
    
    if type_filter:
        query = query.join(models.Pokemon.types).filter(models.Type.name == type_filter)
    
    pokemon_list = query.offset(skip).limit(limit).all()
    
    # Converting to dictionaries that match the schema exactly
    result = []
    for pokemon in pokemon_list:
        pokemon_dict = {
            "id": pokemon.id,
            "name": pokemon.name,
            "height": pokemon.height,
            "weight": pokemon.weight,
            "base_experience": pokemon.base_experience,
            "sprite_url": pokemon.sprite_url,
            "official_artwork_url": getattr(pokemon, 'official_artwork_url', pokemon.sprite_url),
            "types": [{"id": type.id, "name": type.name} for type in pokemon.types],
            "abilities": [{"id": ability.id, "name": ability.name} for ability in pokemon.abilities],
            "stats": [{"id": stat.id, "name": stat.name, "base_stat": stat.base_stat, "effort": stat.effort} for stat in pokemon.stats]
        }
        result.append(pokemon_dict)
    
    return result
#Get a specific Pokemon by ID
@app.get("/pokemon/{pokemon_id}", response_model=schemas.Pokemon)
def get_pokemon_by_id(pokemon_id: int, db: Session = Depends(get_db)):
    
    pokemon = db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id).first()
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    
    pokemon_dict = {
        "id": pokemon.id,
        "name": pokemon.name,
        "height": pokemon.height,
        "weight": pokemon.weight,
        "base_experience": pokemon.base_experience,
        "sprite_url": pokemon.sprite_url,
        "official_artwork_url": getattr(pokemon, 'official_artwork_url', pokemon.sprite_url),
        "types": [{"id": type.id, "name": type.name} for type in pokemon.types],
        "abilities": [{"id": ability.id, "name": ability.name} for ability in pokemon.abilities],
        "stats": [{"id": stat.id, "name": stat.name, "base_stat": stat.base_stat, "effort": stat.effort} for stat in pokemon.stats]
    }
    return pokemon_dict

#Get a specific Pokemon by name
@app.get("/pokemon/name/{pokemon_name}", response_model=schemas.Pokemon)
def get_pokemon_by_name(pokemon_name: str, db: Session = Depends(get_db)):
    
    pokemon = db.query(models.Pokemon).filter(models.Pokemon.name == pokemon_name).first()
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    
    pokemon_dict = {
        "id": pokemon.id,
        "name": pokemon.name,
        "height": pokemon.height,
        "weight": pokemon.weight,
        "base_experience": pokemon.base_experience,
        "sprite_url": pokemon.sprite_url,
        "official_artwork_url": getattr(pokemon, 'official_artwork_url', pokemon.sprite_url),
        "types": [{"id": type.id, "name": type.name} for type in pokemon.types],
        "abilities": [{"id": ability.id, "name": ability.name} for ability in pokemon.abilities],
        "stats": [{"id": stat.id, "name": stat.name, "base_stat": stat.base_stat, "effort": stat.effort} for stat in pokemon.stats]
    }
    return pokemon_dict
#Get all available Pokemon types
@app.get("/types/", response_model=List[schemas.TypeBase])
def get_types(db: Session = Depends(get_db)):
   
    types = db.query(models.Type).all()
    return [{"id": type.id, "name": type.name} for type in types]

#Health check endpoint
@app.get("/health/")
def health_check():
    
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
