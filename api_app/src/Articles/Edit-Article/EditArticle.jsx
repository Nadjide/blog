import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom'; 
import { TextField, Button, Box, Paper, Container, Typography } from '@mui/material';
//import { AuthContext } from '../../AuthContext';

export default function EditArticle() {
  const { article_id } = useParams();
  const navigate = useNavigate();
  const [article, setArticle] = useState(null);
  //const { user } = useContext(AuthContext);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/articles/${article_id}`)
      .then(response => response.json())
      .then(data => setArticle(data));
  }, [article_id]);

  const handleInputChange = (event) => {
    setArticle({ ...article, [event.target.name]: event.target.value });
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    fetch(`http://127.0.0.1:8000/articles/${article_id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(article),
    })
      .then(response => response.json())
      .then(() => navigate('/'));
  };

  return (
    <Container maxWidth="sm">
      <Paper elevation={3} sx={{ mt: 5, p: 3 }}>
        <Typography variant="h4" sx={{ mb: 3, textAlign: 'center' }}>
          Edit Article
        </Typography>
        <Box
          component="form"
          onSubmit={handleSubmit}
          sx={{
            '& .MuiTextField-root': { mb: 2, width: '100%' },
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
          }}
        >
          <TextField
            label="Title"
            name="title"
            value={article?.title || ''}
            onChange={handleInputChange}
            variant="outlined"
          />
          <TextField
            label="Content"
            name="content"
            value={article?.content || ''}
            onChange={handleInputChange}
            variant="outlined"
            multiline
            rows={4}
          />
          <Button type="submit" variant="contained" color="primary" sx={{ mt: 2 }}>
            Update Article
          </Button>
        </Box>
      </Paper>
    </Container>
  );
}
