import React, { useState, useContext } from "react";
import { Box, TextField, Button, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";
import { AuthContext } from "../../AuthContext";

function CreateArticle() {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const navigate = useNavigate();
  const { user } = useContext(AuthContext);

  const handleSubmit = (event) => {
    event.preventDefault();

    if (!user || !user.username) {
      console.error("User information is missing");
      return;
    }

    const slug = title.toLowerCase().replace(/\s+/g, "-");

    fetch("http://127.0.0.1:8000/articles", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        title: title,
        author: user.username,
        content: content,
        slug: slug,
        date: new Date().toISOString(),
        user_id: user.id,
      }),
    })
      .then((response) => {
        if (!response.ok) {
          console.log(response.json());
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        console.log("Success:", data);
        navigate("/");
      })
      .catch((error, data) => {
        console.error("Error:", error);
      });
  };

  return (
    <Box
      component="form"
      onSubmit={handleSubmit}
      sx={{
        display: "flex",
        flexDirection: "column",
        gap: 2,
        maxWidth: "500px",
        margin: "0 auto",
        padding: "20px",
        border: "1px solid #ccc",
        borderRadius: "5px",
      }}
    >
      <Typography variant="h4" sx={{ mb: 4 }}>
        Create Article
      </Typography>
      <TextField
        label="Title"
        value={title}
        onChange={(e) => setTitle(e.target.value)}
        fullWidth
      />
      <TextField
        label="Content"
        value={content}
        onChange={(e) => setContent(e.target.value)}
        fullWidth
        multiline
        rows={4}
      />
      <Button type="submit" variant="contained" sx={{ marginTop: 2 }}>
        Submit
      </Button>
    </Box>
  );
}

export default CreateArticle;
