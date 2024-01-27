import React, { useEffect, useState } from "react";
import { useContext } from "react";
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  CardActions,
} from "@mui/material";
import { Link } from "react-router-dom";
import ArticleIcon from "@mui/icons-material/Article";
import EditIcon from "@mui/icons-material/Edit";
import { AuthContext } from "../../AuthContext";

export default function ArticleList() {
  const [articles, setArticles] = useState([]);
  const { user } = useContext(AuthContext);

  useEffect(() => {
    fetch("http://127.0.0.1:8000/articles")
      .then((response) => response.json())
      .then((data) => setArticles(data));
  }, []);

  return (
    <Box
      sx={{
        padding: "20px",
        maxWidth: "800px",
        margin: "auto",
      }}
    >
      <Typography variant="h4" sx={{ mb: 4, textAlign: "center" }}>
        Articles List
      </Typography>
      <Box sx={{ display: "flex", justifyContent: "flex-end", mb: 2 }}>
        <Button
          variant="contained"
          color="primary"
          startIcon={<ArticleIcon />}
          component={Link}
          to="/create-article"
        >
          Créer un article
        </Button>
      </Box>
      {articles.map((article) => (
        <Card
          key={article.id}
          sx={{
            marginBottom: "20px",
            "&:hover": {
              boxShadow: "0px 8px 24px rgba(0,0,0,0.2)",
              ".MuiCardActions-root": { backgroundColor: "rgba(0,0,0,0.04)" },
            },
          }}
        >
          <CardContent>
            <Typography
              variant="h5"
              sx={{ fontWeight: "bold", marginBottom: "8px" }}
            >
              {article.title}
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 1.5 }}>
              Par {article.author} - {article.date}
            </Typography>
            <Typography variant="body1">{article.content}</Typography>
          </CardContent>
          <CardActions disableSpacing>
            <Button
              size="small"
              color="primary"
              component={Link}
              to={`/article/${article.id}`}
            >
              Lire plus
            </Button>
            {user && user.id === article.user_id && (
              <Button
                size="small"
                startIcon={<EditIcon />}
                component={Link}
                to={`/edit-article/${article.id}`}
              >
                Edit
              </Button>
            )}
          </CardActions>
        </Card>
      ))}
    </Box>
  );
}
