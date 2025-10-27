import React from 'react';

const SearchFilter = ({ types, selectedType, onTypeChange }) => {
  return (
    <div className="search-filter">
      <select 
        value={selectedType} 
        onChange={(e) => onTypeChange(e.target.value)}
        className="type-filter"
      >
        <option value="">All Types</option>
        {types.map(type => (
          <option key={type.id} value={type.name}>
            {type.name.charAt(0).toUpperCase() + type.name.slice(1)}
          </option>
        ))}
      </select>
    </div>
  );
};

export default SearchFilter;