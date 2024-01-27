import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "./App.css";
import Header from "./header/Header";
import ArticleList from "./Articles/ArticleList/ArticleList";
import EditArticle from "./Articles/Edit-Article/EditArticle";
import Login from "./Login/Login";
import Register from "./Register/Register";
import CreateArticle from "./Articles/CreateArticle/create-article";
import ArticleDetail from "./Articles/ArticleDetail/ArticleDetail";
import { AuthProvider } from "./AuthContext";

function App() {
  return (
    <AuthProvider>
      <Router>
        <div>
          <Header />
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/Register" element={<Register />} />
            <Route path="/" element={<ArticleList />} />
            <Route path="/create-article" element={<CreateArticle />} />
            <Route path="/edit-article/:article_id" element={<EditArticle />} />
            <Route path="/article/:id" element={<ArticleDetail />} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
