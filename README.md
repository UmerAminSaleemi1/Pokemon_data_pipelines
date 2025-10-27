# Pokemon Data Pipeline

A complete ETL (Extract, Transform, Load) pipeline that fetches Pokemon data from the public PokeAPI, transforms it into a structured format, and stores it in a PostgreSQL database with a React frontend for data visualization.

##  Features

- **ETL Pipeline**: Extract data from PokeAPI, transform nested JSON into structured format, load into PostgreSQL
- **RESTful API**: FastAPI backend with comprehensive endpoints for data access
- **Interactive Frontend**: React-based web interface with filtering and search capabilities
- **Containerized**: Docker support for easy deployment
- **Robust Error Handling**: Comprehensive logging and error recovery

##  Tech Stack

- **Backend**: FastAPI, SQLAlchemy, PostgreSQL, Pydantic
- **Frontend**: React, CSS3
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Containerization**: Docker, Docker Compose
- **API**: RESTful design with automatic OpenAPI documentation

## Architecture & Design Choices

### Database Schema Design

I designed a **normalized relational schema** to efficiently store Pokemon data:

```sql
-- Core entities
pokemon (id, name, height, weight, base_experience, sprite_url, official_artwork_url)
types (id, name)
abilities (id, name)  
stats (id, name, base_stat, effort, pokemon_id)

-- Many-to-many relationships
pokemon_types (pokemon_id, type_id)
pokemon_abilities (pokemon_id, ability_id)
```
## Assumptions Made

Data Stability: PokeAPI responses follow consistent schema

Network Reliability: Implemented retry logic for transient failures

Database Availability: PostgreSQL is running and accessible

Data Volume: Pipeline processes 20 Pokemon initially (easily scalable)

User Experience: Frontend focuses on core browsing and filtering


### **Potential Future Improvements**

The project successfully delivers all **core requirements** and several **optional components**. The main areas for improvement from the original project description are:

1. **GraphQL API** (mentioned as optional but not implemented)
2. **Comprehensive testing** (mentioned under "Pythonic & Robust Code")
3. **Enhanced containerization** (basic implementation exists)
4. **More complex data transformations** (basic implementation exists)
## Quick Start
### Prerequisites
- Python 3.9+
- Node.js 16+
- PostgreSQL 13+ (or use Docker)
#### 1. Database Setup
```bash
# Create database (if not exists)
createdb pokemon_db

# Or using psql
psql -U postgres -c "CREATE DATABASE pokemon_db;"
```
#### 2. Backend
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
#### 3. Frontend
```bash
# New terminal
cd frontend

# Install dependencies
npm install

# Start frontend
npm start
```

