import React from 'react';
import './App.css';
import UploadPage from './pages/UploadPage';

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <h1>Chemistry Paper Translator</h1>
        <p>Translate chemistry research papers with context awareness</p>
      </header>
      <main>
        <UploadPage />
      </main>
    </div>
  );
}

export default App;
