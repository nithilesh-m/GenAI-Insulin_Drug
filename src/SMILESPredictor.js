import React, { useState } from 'react';
import { predictSMILES } from './utils/modelUtils';

function SMILESPredictor() {
  const [proteinSequence, setProteinSequence] = useState('');
  const [smilesResult, setSmilesResult] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  // Valid amino acid characters
  const validAminoAcids = 'ACDEFGHIKLMNPQRSTVWY';

  const handleInputChange = (e) => {
    const value = e.target.value.toUpperCase();
    // Filter out invalid characters and limit to 50 characters
    const filteredValue = value
      .split('')
      .filter(char => validAminoAcids.includes(char))
      .join('')
      .slice(0, 50);
    
    setProteinSequence(filteredValue);
    setError('');
    setSuccess('');
  };

  const handlePredict = async () => {
    if (proteinSequence.length !== 50) {
      setError('Please enter exactly 50 amino acid characters.');
      return;
    }

    setIsLoading(true);
    setError('');
    setSuccess('');
    setSmilesResult('');

    try {
      const result = await predictSMILES(proteinSequence);
      setSmilesResult(result);
      setSuccess('SMILES prediction completed successfully!');
    } catch (err) {
      setError(`Prediction failed: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(smilesResult);
      setSuccess('SMILES copied to clipboard!');
      setTimeout(() => setSuccess(''), 3000);
    } catch (err) {
      setError('Failed to copy to clipboard');
    }
  };

  const getCharacterCountClass = () => {
    if (proteinSequence.length === 50) return 'success';
    if (proteinSequence.length > 40) return 'warning';
    return '';
  };

  return (
    <div className="container">
      <div className="header">
        <h1>Protein to SMILES Predictor</h1>
        <p>
          Enter a 50-character mutated protein sequence to predict its corresponding drug SMILES structure. 
          Our AI model will analyze the protein sequence and generate a valid drug molecule representation.
        </p>
      </div>

      <div className="main-card">
        <div className="input-section">
          <div className="input-group">
            <label htmlFor="protein-sequence" className="label">
              Protein Sequence (50 amino acids)
            </label>
            <input
              id="protein-sequence"
              type="text"
              className="input-field"
              placeholder="Enter 50 amino acid sequence (e.g., ACDEFGHIKLMNPQRSTVWYACDEFGHIKLMNPQRSTVWYACDEFGHIKLMNPQRSTVWYACDEFGHIKLMNPQRSTVWYACDEFGHIKLMNPQRSTVWY)"
              value={proteinSequence}
              onChange={handleInputChange}
              maxLength={50}
            />
            <div className={`character-count ${getCharacterCountClass()}`}>
              {proteinSequence.length}/50 characters
            </div>
          </div>

          <button
            className="predict-button"
            onClick={handlePredict}
            disabled={isLoading || proteinSequence.length !== 50}
          >
            {isLoading && <span className="loading"></span>}
            {isLoading ? 'Predicting...' : 'Predict SMILES'}
          </button>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {success && !smilesResult && (
          <div className="success-message">
            {success}
          </div>
        )}

        {smilesResult && (
          <div className="results-section">
            <h3 className="results-title">Predicted SMILES Structure</h3>
            <div className="smiles-output">
              {smilesResult}
            </div>
            <button className="copy-button" onClick={copyToClipboard}>
              Copy SMILES
            </button>
          </div>
        )}
      </div>
    </div>
  );
}

export default SMILESPredictor;
