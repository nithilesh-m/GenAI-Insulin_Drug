import React, { useState } from 'react';
import { generateSimilarSequences } from './utils/sequenceUtils';

function SequenceGenerator() {
  const [proteinSequence, setProteinSequence] = useState('');
  const [generatedSequences, setGeneratedSequences] = useState([]);
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

  const handleGenerate = async () => {
    if (proteinSequence.length !== 50) {
      setError('Please enter exactly 50 amino acid characters.');
      return;
    }

    setIsLoading(true);
    setError('');
    setSuccess('');
    setGeneratedSequences([]);

    try {
      const result = await generateSimilarSequences(proteinSequence);
      setGeneratedSequences(result);
      setSuccess('Successfully generated 5 similar protein sequences!');
    } catch (err) {
      setError(`Generation failed: ${err.message}`);
    } finally {
      setIsLoading(false);
    }
  };

  const copyToClipboard = async (sequence) => {
    try {
      await navigator.clipboard.writeText(sequence);
      setSuccess('Sequence copied to clipboard!');
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
        <h1>Protein Sequence Generator</h1>
        <p>
          Enter a 50-character mutated protein sequence to generate 5 similar sequences 
          with the highest BLOSUM62 scores. Our AI model will analyze the input sequence 
          and generate the most similar mutated variants.
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
            onClick={handleGenerate}
            disabled={isLoading || proteinSequence.length !== 50}
          >
            {isLoading && <span className="loading"></span>}
            {isLoading ? 'Generating...' : 'Generate Similar Sequences'}
          </button>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        {success && !generatedSequences.length && (
          <div className="success-message">
            {success}
          </div>
        )}

        {generatedSequences.length > 0 && (
          <div className="results-section">
            <h3 className="results-title">Top 5 Similar Sequences (by BLOSUM62 Score)</h3>
            <div className="sequences-container">
              {generatedSequences.map((item, index) => (
                <div key={index} className="sequence-item">
                  <div className="sequence-header">
                    <span className="sequence-rank">#{index + 1}</span>
                    <span className="blosum-score">BLOSUM62 Score: {item.score.toFixed(2)}</span>
                  </div>
                  <div className="sequence-output">
                    {item.sequence}
                  </div>
                  <button 
                    className="copy-button" 
                    onClick={() => copyToClipboard(item.sequence)}
                  >
                    Copy Sequence
                  </button>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default SequenceGenerator;
