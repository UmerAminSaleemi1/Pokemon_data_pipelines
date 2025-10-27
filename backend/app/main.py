from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, pipeline
from .database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Pokémon Data Pipeline", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize pipeline
pokemon_pipeline = pipeline.PokemonPipeline()

@app.post("/pokemon/run-pipeline/")
def run_pipeline(
    start_id: int = 1,
    end_id: int = 20,
    db: Session = Depends(get_db)
):
    """Trigger the ETL pipeline"""
    result = pokemon_pipeline.run_pipeline(db, start_id, end_id)
    return result

@app.get("/pokemon/", response_model=List[schemas.Pokemon])
def get_pokemon(
    skip: int = 0,
    limit: int = 20,
    type_filter: str = None,
    db: Session = Depends(get_db)
):
    """Get all Pokémon with optional filtering"""
    query = db.query(models.Pokemon)
    
    if type_filter:
        query = query.join(models.Pokemon.types).filter(models.Type.name == type_filter)
    
    pokemon = query.offset(skip).limit(limit).all()
    return pokemon

@app.get("/pokemon/{pokemon_id}", response_model=schemas.Pokemon)
def get_pokemon_by_id(pokemon_id: int, db: Session = Depends(get_db)):
    """Get a specific Pokémon by ID"""
    pokemon = db.query(models.Pokemon).filter(models.Pokemon.id == pokemon_id).first()
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon not found")
    return pokemon

@app.get("/pokemon/name/{pokemon_name}", response_model=schemas.Pokemon)
def get_pokemon_by_name(pokemon_name: str, db: Session = Depends(get_db)):
    """Get a specific Pokémon by name"""
    pokemon = db.query(models.Pokemon).filter(models.Pokemon.name == pokemon_name).first()
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokémon not found")
    return pokemon

@app.get("/types/", response_model=List[schemas.Type])
def get_types(db: Session = Depends(get_db)):
    """Get all available Pokémon types"""
    types = db.query(models.Type).all()
    return types

@app.get("/health/")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)