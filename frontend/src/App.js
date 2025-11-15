import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SearchPage from './pages/SearchPage';
import './styles/index.css';

function App() {
  return (
    <Router basename="/college-scrap">
      <div className="app-container">
        <Routes>
          <Route path="/" element={<SearchPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
