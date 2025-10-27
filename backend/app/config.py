import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # PostgreSQL connection
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:12345@localhost:5432/pokemon_db"
    )
    POKEAPI_BASE_URL: str = "https://pokeapi.co/api/v2"

settings = Settings()