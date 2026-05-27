// import { useState } from "react";
import ChatPage from "./pages/ChatPage";
import DashboardPage from "./pages/DashboardPage";
import RepoPage from "./pages/RepoPage";
import LoginPage from "./pages/LoginPage";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import "./App.css";

function App() {
  return (
    <>
      <Router>
        <Routes>
          <Route path="/" element={<LoginPage />} />
          <Route path="/chat" element={<ChatPage />} />
          <Route path="/dashboard" element={<DashboardPage />} />
          <Route path="/repo/:id" element={<RepoPage />} />
        </Routes>
      </Router>
    </>
  );
}

export default App;
