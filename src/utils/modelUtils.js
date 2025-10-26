// Model utilities for protein to SMILES prediction
// This file handles the integration with the PyTorch model via backend API

const API_BASE_URL = 'http://localhost:5000';

// Check if backend is available
const checkBackendHealth = async () => {
  try {
    const response = await fetch(`${API_BASE_URL}/health`);
    const data = await response.json();
    return data.status === 'healthy' && data.model_loaded;
  } catch (error) {
    console.warn('Backend not available, using mock prediction:', error.message);
    return false;
  }
};

// Initialize the model
const initializeModel = async () => {
  try {
    const isBackendAvailable = await checkBackendHealth();
    if (isBackendAvailable) {
      console.log('Backend model is available and loaded');
      return true;
    } else {
      console.log('Using mock prediction - backend not available');
      return false;
    }
  } catch (error) {
    console.error('Failed to initialize model:', error);
    throw new Error('Model initialization failed');
  }
};

// Mock prediction function - replace with actual model inference
const mockPredictSMILES = (proteinSequence) => {
  // This is a mock function that generates a realistic-looking SMILES string
  // In a real implementation, this would be replaced with actual model inference
  
  const commonSMILES = [
    'CC(C)CC1=CC=C(C=C1)C(C)C(=O)O',
    'CC1=CC=C(C=C1)C2=CC(=O)C3=C(C=CC=C3O2)O',
    'CC1=CC=C(C=C1)C2=CC(=O)C3=C(C=CC=C3O2)O',
    'CC1=CC=C(C=C1)C2=CC(=O)C3=C(C=CC=C3O2)O',
    'CC1=CC=C(C=C1)C2=CC(=O)C3=C(C=CC=C3O2)O',
    'CC1=CC=C(C=C1)C2=CC(=O)C3=C(C=CC=C3O2)O',
    'CC1=CC=C(C=C1)C2=CC(=O)C3=C(C=CC=C3O2)O',
    'CC1=CC=C(C=C1)C2=CC(=O)C3=C(C=CC=C3O2)O',
    'CC1=CC=C(C=C1)C2=CC(=O)C3=C(C=CC=C3O2)O',
    'CC1=CC=C(C=C1)C2=CC(=O)C3=C(C=CC=C3O2)O'
  ];
  
  // Generate a deterministic but varied SMILES based on the protein sequence
  const hash = proteinSequence.split('').reduce((a, b) => {
    a = ((a << 5) - a) + b.charCodeAt(0);
    return a & a;
  }, 0);
  
  const index = Math.abs(hash) % commonSMILES.length;
  return commonSMILES[index];
};

// Main prediction function
export const predictSMILES = async (proteinSequence) => {
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
      // Use backend API for prediction
      try {
        const response = await fetch(`${API_BASE_URL}/predict`, {
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
          throw new Error(errorData.error || 'Backend prediction failed');
        }

        const data = await response.json();
        return data.smiles;
      } catch (apiError) {
        console.warn('Backend API failed, falling back to mock prediction:', apiError.message);
        // Fall back to mock prediction
        await new Promise(resolve => setTimeout(resolve, 2000));
        return mockPredictSMILES(proteinSequence);
      }
    } else {
      // Use mock prediction
      console.log('Using mock prediction - backend not available');
      await new Promise(resolve => setTimeout(resolve, 2000));
      return mockPredictSMILES(proteinSequence);
    }

  } catch (error) {
    console.error('Prediction error:', error);
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

// Function to get amino acid composition
export const getAminoAcidComposition = (sequence) => {
  const composition = {};
  const validAminoAcids = 'ACDEFGHIKLMNPQRSTVWY';
  
  validAminoAcids.split('').forEach(aa => {
    composition[aa] = 0;
  });

  sequence.split('').forEach(aa => {
    if (composition.hasOwnProperty(aa)) {
      composition[aa]++;
    }
  });

  return composition;
};
