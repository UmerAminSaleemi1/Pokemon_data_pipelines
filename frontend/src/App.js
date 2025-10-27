import React, { useState, useEffect } from 'react';
import PokemonList from './components/PokemonList';
import SearchFilter from './components/SearchFilter';
import './App.css';

const API_BASE = 'http://localhost:8000';

function App() {
  const [pokemon, setPokemon] = useState([]);
  const [types, setTypes] = useState([]);
  const [selectedType, setSelectedType] = useState('');
  const [loading, setLoading] = useState(false);
  const [pipelineRunning, setPipelineRunning] = useState(false);

  useEffect(() => {
    fetchTypes();
    fetchPokemon();
  }, [selectedType]);

  const fetchPokemon = async () => {
    setLoading(true);
    try {
      const url = selectedType 
        ? `${API_BASE}/pokemon/?type_filter=${selectedType}`
        : `${API_BASE}/pokemon/`;
      
      const response = await fetch(url);
      const data = await response.json();
      setPokemon(data);
    } catch (error) {
      console.error('Error fetching Pokémon:', error);
    }
    setLoading(false);
  };

  const fetchTypes = async () => {
    try {
      const response = await fetch(`${API_BASE}/types/`);
      const data = await response.json();
      setTypes(data);
    } catch (error) {
      console.error('Error fetching types:', error);
    }
  };

  const runPipeline = async () => {
    setPipelineRunning(true);
    try {
      const response = await fetch(`${API_BASE}/pokemon/run-pipeline/`, {
        method: 'POST'
      });
      const result = await response.json();
      alert(`Pipeline completed! Successful: ${result.successful}, Failed: ${result.failed}`);
      fetchPokemon(); // Refresh the list
    } catch (error) {
      console.error('Error running pipeline:', error);
      alert('Error running pipeline');
    }
    setPipelineRunning(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Pokémon Data Pipeline</h1>
        <button 
          onClick={runPipeline} 
          disabled={pipelineRunning}
          className="pipeline-btn"
        >
          {pipelineRunning ? 'Running Pipeline...' : 'Run Data Pipeline'}
        </button>
      </header>

      <main>
        <SearchFilter 
          types={types}
          selectedType={selectedType}
          onTypeChange={setSelectedType}
        />
        
        {loading ? (
          <div className="loading">Loading Pokémon...</div>
        ) : (
          <PokemonList pokemon={pokemon} />
        )}
      </main>
    </div>
  );
}

export default App;