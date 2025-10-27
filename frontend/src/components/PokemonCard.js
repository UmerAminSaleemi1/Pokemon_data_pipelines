import React from 'react';

const typeColors = {
  normal: '#A8A878',
  fire: '#F08030',
  water: '#6890F0',
  electric: '#F8D030',
  grass: '#78C850',
  ice: '#98D8D8',
  fighting: '#C03028',
  poison: '#A040A0',
  ground: '#E0C068',
  flying: '#A890F0',
  psychic: '#F85888',
  bug: '#A8B820',
  rock: '#B8A038',
  ghost: '#705898',
  dragon: '#7038F8',
  dark: '#705848',
  steel: '#B8B8D0',
  fairy: '#EE99AC'
};

const PokemonCard = ({ pokemon }) => {
  return (
    <div className="pokemon-card">
      <div className="pokemon-name">{pokemon.name}</div>
      <img 
        src={pokemon.official_artwork_url || pokemon.sprite_url} 
        alt={pokemon.name}
        className="pokemon-image"
        onError={(e) => {
          e.target.src = 'https://via.placeholder.com/120x120?text=No+Image';
        }}
      />
      
      <div className="pokemon-types">
        {pokemon.types.map(type => (
          <span 
            key={type.id}
            className="type-badge"
            style={{ backgroundColor: typeColors[type.name] || '#777' }}
          >
            {type.name}
          </span>
        ))}
      </div>

      <div className="pokemon-stats">
        <div className="stat-row">
          <span className="stat-name">Height:</span>
          <span className="stat-value">{pokemon.height / 10}m</span>
        </div>
        <div className="stat-row">
          <span className="stat-name">Weight:</span>
          <span className="stat-value">{pokemon.weight / 10}kg</span>
        </div>
        <div className="stat-row">
          <span className="stat-name">Base EXP:</span>
          <span className="stat-value">{pokemon.base_experience}</span>
        </div>
        
        {pokemon.stats.map(stat => (
          <div key={stat.id} className="stat-row">
            <span className="stat-name">{stat.name}:</span>
            <span className="stat-value">{stat.base_stat}</span>
          </div>
        ))}
      </div>
    </div>
  );
};

export default PokemonCard;