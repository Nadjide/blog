import React, { useState, useEffect } from 'react';
import { TextField, Box } from '@mui/material';

export default function SearchBar({ setArticles }) {
  const [search, setSearch] = useState('');

  useEffect(() => {
    if (search) {
      fetch(`http://127.0.0.1:8000/articles/search/${search}`)
        .then((response) => response.json())
        .then((data) => setArticles(data));
    } else {
      fetch("http://127.0.0.1:8000/articles")
        .then((response) => response.json())
        .then((data) => setArticles(data));
    }
  }, [search, setArticles]);

  return (
    <Box sx={{ mb: 2 }}>
      <TextField
        fullWidth
        label="Search"
        variant="outlined"
        value={search}
        onChange={(e) => setSearch(e.target.value)}
      />
    </Box>
  );
}