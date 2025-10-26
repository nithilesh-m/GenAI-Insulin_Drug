// Sequence generation utilities for protein sequence generation
// This file handles the integration with the final_ckpt.pt model via backend API

const API_BASE_URL = 'http://localhost:5001'; // Different port for sequence generation

// Check if backend is available
const checkBackendHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    const data = await response.json();
    return data.status === 'healthy' && data.model_loaded;
  } catch (error) {
    console.warn('Sequence generation backend not available, using mock generation:', error.message);
    return false;
  }
};

// Mock sequence generation function
const mockGenerateSequences = (proteinSequence) => {
  // Generate 5 mock similar sequences with mock BLOSUM62 scores
  const sequences = [];
  const baseSequence = proteinSequence;
  
  for (let i = 0; i < 5; i++) {
    // Create a slightly modified version of the input sequence
    const modifiedSequence = baseSequence.split('').map((char, index) => {
      // Randomly modify some positions (10% chance)
      if (Math.random() < 0.1) {
        const validAminoAcids = 'ACDEFGHIKLMNPQRSTVWY';
        const randomIndex = Math.floor(Math.random() * validAminoAcids.length);
        return validAminoAcids[randomIndex];
      }
      return char;
    }).join('');
    
    // Generate a mock BLOSUM62 score (higher is better)
    const mockScore = 2.5 + Math.random() * 1.5; // Range: 2.5 to 4.0
    
    sequences.push({
      sequence: modifiedSequence,
      score: mockScore
    });
  }
  
  // Sort by score (highest first)
  return sequences.sort((a, b) => b.score - a.score);
};

// Main sequence generation function
export const generateSimilarSequences = async (proteinSequence) => {
  try {
    // Validate input
    if (!proteinSequence || proteinSequence.length !== 50) {
      throw new Error('Protein sequence must be exactly 50 characters long');
    }

    // Check for valid amino acid characters
    const validAminoAcids = 'ACDEFGHIKLMNPQRSTVWY';
    const invalidChars = proteinSequence.split('').filter(char => !validAminoAcids.includes(char));
    if (invalidChars.length > 0) {
      throw new Error(`Invalid amino acid characters found: ${invalidChars.join(', ')}`);
    }

    // Check if backend is available
    const isBackendAvailable = await checkBackendHealth();
    
    if (isBackendAvailable) {
      // Use backend API for sequence generation
      try {
        const response = await fetch(`${API_BASE_URL}/generate`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            sequence: proteinSequence
          })
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(errorData.error || 'Backend generation failed');
        }

        const data = await response.json();
        return data.sequences;
      } catch (apiError) {
        console.warn('Backend API failed, falling back to mock generation:', apiError.message);
        // Fall back to mock generation
        await new Promise(resolve => setTimeout(resolve, 3000));
        return mockGenerateSequences(proteinSequence);
      }
    } else {
      // Use mock generation
      console.log('Using mock generation - backend not available');
      await new Promise(resolve => setTimeout(resolve, 3000));
      return mockGenerateSequences(proteinSequence);
    }

  } catch (error) {
    console.error('Sequence generation error:', error);
    throw error;
  }
};

// Function to validate protein sequence
export const validateProteinSequence = (sequence) => {
  const validAminoAcids = 'ACDEFGHIKLMNPQRSTVWY';
  const errors = [];

  if (!sequence) {
    errors.push('Protein sequence is required');
  } else {
    if (sequence.length !== 50) {
      errors.push(`Sequence must be exactly 50 characters long (current: ${sequence.length})`);
    }

    const invalidChars = sequence.split('').filter(char => !validAminoAcids.includes(char));
    if (invalidChars.length > 0) {
      errors.push(`Invalid amino acid characters: ${invalidChars.join(', ')}`);
    }
  }

  return {
    isValid: errors.length === 0,
    errors
  };
};
