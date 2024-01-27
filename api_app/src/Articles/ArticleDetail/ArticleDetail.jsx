import React, { useEffect, useState, useContext } from "react";
import { useParams } from "react-router-dom";
import { AuthContext } from "../../AuthContext";
import {
  Box,
  Typography,
  Card,
  CardContent,
  TextField,
  Button,
  CircularProgress,
} from "@mui/material";

export default function ArticleDetail() {
  const { id } = useParams();
  const [article, setArticle] = useState(null);
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState("");
  const { user } = useContext(AuthContext);
  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/articles/${id}`)
      .then((response) => response.json())
      .then((data) => setArticle(data));

    fetch(`http://127.0.0.1:8000/articles/${id}/comments`)
      .then((response) => response.json())
      .then((data) => setComments(data));
  }, [id]);

  const handleCommentChange = (event) => {
    setNewComment(event.target.value);
  };

  const handleCommentSubmit = () => {
    if (!user) {
      alert("Vous devez être connecté pour poster un commentaire");
      return;
    }
    setIsSubmitting(true);
    fetch(`http://127.0.0.1:8000/articles/${id}/comments`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        content: newComment,
        date: new Date().toISOString().slice(0, 10),
        user_id: user.id,
        article_id: id,
        username: user.username,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        setComments((prevComments) => [...prevComments, data]);
        console.log("Comment submitted:", data);
      })
      .finally(() => {
        setIsSubmitting(false);
      });

    setNewComment("");
  };

  if (!article) {
    return (
      <Box display="flex" justifyContent="center" mt={5}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ padding: "20px", maxWidth: "800px", margin: "auto" }}>
      <Card
        sx={{
          marginBottom: "20px",
          backgroundColor: "#f9f9f9",
          boxShadow: "0px 2px 4px rgba(0,0,0,0.1)",
        }}
      >
        <CardContent>
          <Typography
            variant="h4"
            sx={{ fontWeight: "bold", marginBottom: "8px" }}
          >
            {article.title}
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ mb: 1.5 }}>
            Par {article.author} - {new Date(article.date).toLocaleDateString()}
          </Typography>
          <Typography variant="body1">{article.content}</Typography>
        </CardContent>
      </Card>
      <Box sx={{ my: 4 }}>
        <Typography variant="h6" sx={{ mb: 2 }}>
          Nouveau Commentaire
        </Typography>
        <TextField
          label="Commentaire"
          variant="outlined"
          fullWidth
          multiline
          rows={4}
          value={newComment}
          onChange={handleCommentChange}
          sx={{ mb: 2 }}
        />
        <Button
          variant="contained"
          color="primary"
          disabled={isSubmitting}
          onClick={handleCommentSubmit}
          sx={{ display: 'block' }}
        >
          {isSubmitting ? <CircularProgress size={24} /> : "Envoyer"}
        </Button>
      </Box>
      {comments.length > 0 ? (
        comments.map((comment) => (
          <Card key={comment.id} sx={{ my: 2, backgroundColor: "#f0f0f0", boxShadow: "0px 2px 4px rgba(0,0,0,0.1)" }}>
            <CardContent>
              <Typography variant="body1">{comment.content}</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Par {comment.username} - {new Date(comment.date).toLocaleDateString()}
              </Typography>
            </CardContent>
          </Card>
        ))
      ) : (
        <Typography variant="subtitle1" sx={{ mt: 3, textAlign: 'center' }}>
          Aucun commentaire , soyez le premier à commenter !
        </Typography>
      )}
    </Box>
  );
}
