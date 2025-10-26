import React, { useState } from 'react';
import SMILESPredictor from './SMILESPredictor';
import SequenceGenerator from './SequenceGenerator';

function App() {
  const [currentPage, setCurrentPage] = useState('smiles'); // 'smiles' or 'sequences'

  return (
    <div className="app">
      <nav className="nav-bar">
        <div className="nav-container">
          <h1 className="nav-title">Protein AI Tools</h1>
          <div className="nav-buttons">
            <button 
              className={`nav-button ${currentPage === 'smiles' ? 'active' : ''}`}
              onClick={() => setCurrentPage('smiles')}
            >
              SMILES Predictor
            </button>
            <button 
              className={`nav-button ${currentPage === 'sequences' ? 'active' : ''}`}
              onClick={() => setCurrentPage('sequences')}
            >
              Sequence Generator
            </button>
          </div>
        </div>
      </nav>

      {currentPage === 'smiles' && <SMILESPredictor />}
      {currentPage === 'sequences' && <SequenceGenerator />}
    </div>
  );
}

export default App;
