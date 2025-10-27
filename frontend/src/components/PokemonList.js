import React from 'react';
import PokemonCard from './PokemonCard';

const PokemonList = ({ pokemon }) => {
  if (!pokemon.length) {
    return <div className="loading">No Pokémon found. Run the pipeline first!</div>;
  }

  return (
    <div className="pokemon-grid">
      {pokemon.map(poke => (
        <PokemonCard key={poke.id} pokemon={poke} />
      ))}
    </div>
  );
};

export default PokemonList;