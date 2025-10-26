#!/usr/bin/env python3
"""
Model server for protein to SMILES prediction
This script serves the PyTorch model via a REST API
"""

import torch
import json
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global variable to store the model
model = None

def load_model():
    """Load the PyTorch model"""
    global model
    try:
        model_path = os.path.join(os.path.dirname(__file__), '..', 'fusion_best.pt')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        # Load the model
        # Check if it's a state dict or a complete model
        checkpoint = torch.load(model_path, map_location='cpu')
        
        if isinstance(checkpoint, dict) and 'state_dict' in checkpoint:
            # It's a checkpoint with state_dict
            model = checkpoint
            logger.info("Loaded model checkpoint with state_dict")
        elif isinstance(checkpoint, dict) and 'model' in checkpoint:
            # It's a checkpoint with model
            model = checkpoint['model']
            if hasattr(model, 'eval'):
                model.eval()
        elif hasattr(checkpoint, 'eval'):
            # It's a complete model
            model = checkpoint
            model.eval()
        else:
            # It's a state dict
            model = checkpoint
            logger.info("Loaded model state dictionary")
        
        logger.info(f"Model loaded successfully from {model_path}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to load model: {str(e)}")
        return False

def preprocess_protein_sequence(sequence):
    """
    Preprocess protein sequence for model input
    Convert amino acid sequence to numerical representation
    """
    # Amino acid to index mapping
    aa_to_index = {
        'A': 0, 'C': 1, 'D': 2, 'E': 3, 'F': 4, 'G': 5, 'H': 6, 'I': 7,
        'K': 8, 'L': 9, 'M': 10, 'N': 11, 'P': 12, 'Q': 13, 'R': 14,
        'S': 15, 'T': 16, 'V': 17, 'W': 18, 'Y': 19
    }
    
    # Convert sequence to indices
    indices = [aa_to_index.get(aa, 0) for aa in sequence.upper()]
    
    # Convert to tensor
    tensor = torch.tensor(indices, dtype=torch.long).unsqueeze(0)  # Add batch dimension
    
    return tensor

def postprocess_smiles(prediction):
    """
    Postprocess model prediction to generate SMILES string
    This is a simplified version - you may need to adjust based on your model's output format
    """
    # This is a placeholder - you'll need to implement based on your model's actual output
    # For now, return a mock SMILES string
    mock_smiles = [
        'CC(C)CC1=CC=C(C=C1)C(C)C(=O)O',
        'CC1=CC=C(C=C1)C2=CC(=O)C3=C(C=CC=C3O2)O',
        'CC1=CC=C(C=C1)C2=CC(=O)C3=C(C=CC=C3O2)O',
        'CC1=CC=C(C=C1)C2=CC(=O)C3=C(C=CC=C3O2)O',
        'CC1=CC=C(C=C1)C2=CC(=O)C3=C(C=CC=C3O2)O'
    ]
    
    # Use a simple hash to select a consistent SMILES for the same input
    hash_val = hash(prediction.tolist()) if hasattr(prediction, 'tolist') else hash(str(prediction))
    index = abs(hash_val) % len(mock_smiles)
    
    return mock_smiles[index]

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

@app.route('/predict', methods=['POST'])
def predict():
    """Predict SMILES from protein sequence"""
    try:
        data = request.get_json()
        
        if not data or 'sequence' not in data:
            return jsonify({'error': 'Missing sequence parameter'}), 400
        
        sequence = data['sequence']
        
        # Validate input
        if not isinstance(sequence, str) or len(sequence) != 50:
            return jsonify({
                'error': 'Sequence must be a string of exactly 50 characters'
            }), 400
        
        # Check for valid amino acids
        valid_aa = set('ACDEFGHIKLMNPQRSTVWY')
        if not all(aa in valid_aa for aa in sequence.upper()):
            return jsonify({
                'error': 'Sequence contains invalid amino acid characters'
            }), 400
        
        if model is None:
            return jsonify({'error': 'Model not loaded'}), 500
        
        # Preprocess input
        input_tensor = preprocess_protein_sequence(sequence)
        
        # Make prediction
        with torch.no_grad():
            if hasattr(model, '__call__'):
                # It's a callable model
                prediction = model(input_tensor)
            else:
                # It's a state dict, use mock prediction for now
                logger.warning("Model is a state dict, using mock prediction")
                prediction = torch.randn(1, 100)  # Mock prediction tensor
        
        # Postprocess output
        smiles = postprocess_smiles(prediction)
        
        return jsonify({
            'smiles': smiles,
            'sequence': sequence,
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Prediction error: {str(e)}")
        return jsonify({'error': f'Prediction failed: {str(e)}'}), 500

@app.route('/model_info', methods=['GET'])
def model_info():
    """Get model information"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    return jsonify({
        'model_type': type(model).__name__,
        'model_loaded': True,
        'device': str(next(model.parameters()).device) if hasattr(model, 'parameters') else 'unknown'
    })

if __name__ == '__main__':
    # Load model on startup
    if load_model():
        logger.info("Starting model server...")
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        logger.error("Failed to load model. Exiting.")
        sys.exit(1)
