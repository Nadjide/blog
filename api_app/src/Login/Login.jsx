import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { Box, Button, TextField, Typography, Paper } from "@mui/material";
import { AuthContext } from "../AuthContext";

export default function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [errorMessage, setErrorMessage] = useState(""); 
  const navigate = useNavigate();
  const { setUser } = useContext(AuthContext);

  const handleSubmit = (event) => {
    event.preventDefault();
    fetch("http://127.0.0.1:8000/login", {
      method: "POST",
      headers: {"Content-Type": "application/json",},
      body: JSON.stringify({username: username,password: password,}),
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((data) => {
            throw new Error(data.detail);});
        }return response.json();
      })
      .then((data) => {
        localStorage.setItem("token", data.access_token);
        setUser({username: data.username,id: data.id,});
        navigate("/");
      })
      .catch((error) => {
        setErrorMessage(error.message);
        console.error("Error:", error);
      });
  };

  return (
    <Box
      display="flex"
      flexDirection="column"
      alignItems="center"
      justifyContent="center"
      minHeight="100vh"
    >
      <Paper elevation={3} sx={{ padding: 4, width: "400px" }}>
        <Typography variant="h5" sx={{ marginBottom: 2, textAlign: "center" }}>
          Login
        </Typography>
        {errorMessage && (
          <Typography variant="body2" color="error">
            {errorMessage}
          </Typography>
        )}
        <Box
          component="form"
          onSubmit={handleSubmit}
          sx={{ display: "flex", flexDirection: "column", gap: 2 }}
        >
          <TextField
            label="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            fullWidth
          />
          <TextField
            label="Password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            fullWidth
          />
          <Button
            type="submit"
            variant="contained"
            sx={{ marginTop: 2 }}
            disabled={!username || !password}
          >
            Login
          </Button>
        </Box>
      </Paper>
    </Box>
  );
}