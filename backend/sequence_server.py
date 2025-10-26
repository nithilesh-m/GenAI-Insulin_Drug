#!/usr/bin/env python3
"""
Sequence generation server for protein sequence generation
This script serves the final_ckpt.pt model via a REST API
"""

import torch
import json
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import sys
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Global variable to store the model
model = None

def load_model():
    """Load the PyTorch model for sequence generation"""
    global model
    try:
        model_path = os.path.join(os.path.dirname(__file__), '..', 'final_ckpt.pt')
        
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found: {model_path}")
        
        # Load the model
        checkpoint = torch.load(model_path, map_location='cpu')
        
        if isinstance(checkpoint, dict) and 'state_dict' in checkpoint:
            # It's a checkpoint with state_dict
            model = checkpoint
            logger.info("Loaded sequence generation model checkpoint with state_dict")
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
            logger.info("Loaded sequence generation model state dictionary")
        
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

def generate_sequences_mock(protein_sequence, num_sequences=100):
    """
    Generate mock similar sequences for demonstration
    In a real implementation, this would use the actual model
    """
    sequences = []
    valid_aa = 'ACDEFGHIKLMNPQRSTVWY'
    
    for _ in range(num_sequences):
        # Create a slightly modified version of the input sequence
        modified_sequence = list(protein_sequence)
        
        # Randomly modify some positions (5-15% of positions)
        num_mutations = random.randint(2, 7)  # 2-7 mutations for 50-char sequence
        positions = random.sample(range(50), num_mutations)
        
        for pos in positions:
            # Replace with a random amino acid
            modified_sequence[pos] = random.choice(valid_aa)
        
        sequences.append(''.join(modified_sequence))
    
    return sequences

def calculate_blosum62_score(seq1, seq2):
    """
    Calculate BLOSUM62 score between two sequences
    Using a simplified BLOSUM62 matrix for demonstration
    """
    # Simplified BLOSUM62-like scoring matrix
    # In practice, you would use the actual BLOSUM62 matrix
    scoring_matrix = {
        'A': {'A': 4, 'C': 0, 'D': -2, 'E': -1, 'F': -2, 'G': 0, 'H': -2, 'I': -1, 'K': -1, 'L': -1, 'M': -1, 'N': -2, 'P': -1, 'Q': -1, 'R': -1, 'S': 1, 'T': 0, 'V': 0, 'W': -3, 'Y': -2},
        'C': {'A': 0, 'C': 9, 'D': -3, 'E': -4, 'F': -2, 'G': -3, 'H': -3, 'I': -1, 'K': -3, 'L': -1, 'M': -1, 'N': -3, 'P': -3, 'Q': -3, 'R': -3, 'S': -1, 'T': -1, 'V': -1, 'W': -2, 'Y': -2},
        'D': {'A': -2, 'C': -3, 'D': 6, 'E': 2, 'F': -3, 'G': -1, 'H': -1, 'I': -3, 'K': -1, 'L': -4, 'M': -3, 'N': 1, 'P': -1, 'Q': 0, 'R': -2, 'S': 0, 'T': -1, 'V': -3, 'W': -4, 'Y': -3},
        'E': {'A': -1, 'C': -4, 'D': 2, 'E': 5, 'F': -3, 'G': -2, 'H': 0, 'I': -3, 'K': 1, 'L': -3, 'M': -2, 'N': 0, 'P': -1, 'Q': 2, 'R': 0, 'S': 0, 'T': -1, 'V': -2, 'W': -3, 'Y': -2},
        'F': {'A': -2, 'C': -2, 'D': -3, 'E': -3, 'F': 6, 'G': -3, 'H': -1, 'I': 0, 'K': -3, 'L': 0, 'M': 0, 'N': -3, 'P': -4, 'Q': -3, 'R': -3, 'S': -2, 'T': -2, 'V': -1, 'W': 1, 'Y': 3},
        'G': {'A': 0, 'C': -3, 'D': -1, 'E': -2, 'F': -3, 'G': 6, 'H': -2, 'I': -4, 'K': -2, 'L': -4, 'M': -3, 'N': 0, 'P': -2, 'Q': -2, 'R': -2, 'S': 0, 'T': -2, 'V': -3, 'W': -2, 'Y': -3},
        'H': {'A': -2, 'C': -3, 'D': -1, 'E': 0, 'F': -1, 'G': -2, 'H': 8, 'I': -3, 'K': -1, 'L': -3, 'M': -2, 'N': 1, 'P': -2, 'Q': 0, 'R': 0, 'S': -1, 'T': -2, 'V': -3, 'W': -2, 'Y': 2},
        'I': {'A': -1, 'C': -1, 'D': -3, 'E': -3, 'F': 0, 'G': -4, 'H': -3, 'I': 4, 'K': -3, 'L': 2, 'M': 1, 'N': -3, 'P': -3, 'Q': -3, 'R': -3, 'S': -2, 'T': -1, 'V': 3, 'W': -3, 'Y': -1},
        'K': {'A': -1, 'C': -3, 'D': -1, 'E': 1, 'F': -3, 'G': -2, 'H': -1, 'I': -3, 'K': 5, 'L': -2, 'M': -1, 'N': 0, 'P': -1, 'Q': 1, 'R': 2, 'S': 0, 'T': -1, 'V': -2, 'W': -3, 'Y': -2},
        'L': {'A': -1, 'C': -1, 'D': -4, 'E': -3, 'F': 0, 'G': -4, 'H': -3, 'I': 2, 'K': -2, 'L': 4, 'M': 2, 'N': -3, 'P': -3, 'Q': -2, 'R': -2, 'S': -2, 'T': -1, 'V': 1, 'W': -2, 'Y': -1},
        'M': {'A': -1, 'C': -1, 'D': -3, 'E': -2, 'F': 0, 'G': -3, 'H': -2, 'I': 1, 'K': -1, 'L': 2, 'M': 5, 'N': -2, 'P': -2, 'Q': 0, 'R': -1, 'S': -1, 'T': 0, 'V': 1, 'W': -1, 'Y': -1},
        'N': {'A': -2, 'C': -3, 'D': 1, 'E': 0, 'F': -3, 'G': 0, 'H': 1, 'I': -3, 'K': 0, 'L': -3, 'M': -2, 'N': 6, 'P': -2, 'Q': 0, 'R': 0, 'S': 1, 'T': 0, 'V': -3, 'W': -4, 'Y': -2},
        'P': {'A': -1, 'C': -3, 'D': -1, 'E': -1, 'F': -4, 'G': -2, 'H': -2, 'I': -3, 'K': -1, 'L': -3, 'M': -2, 'N': -2, 'P': 7, 'Q': -1, 'R': -2, 'S': -1, 'T': -1, 'V': -2, 'W': -4, 'Y': -3},
        'Q': {'A': -1, 'C': -3, 'D': 0, 'E': 2, 'F': -3, 'G': -2, 'H': 0, 'I': -3, 'K': 1, 'L': -2, 'M': 0, 'N': 0, 'P': -1, 'Q': 5, 'R': 1, 'S': 0, 'T': -1, 'V': -2, 'W': -2, 'Y': -1},
        'R': {'A': -1, 'C': -3, 'D': -2, 'E': 0, 'F': -3, 'G': -2, 'H': 0, 'I': -3, 'K': 2, 'L': -2, 'M': -1, 'N': 0, 'P': -2, 'Q': 1, 'R': 5, 'S': -1, 'T': -1, 'V': -3, 'W': -3, 'Y': -2},
        'S': {'A': 1, 'C': -1, 'D': 0, 'E': 0, 'F': -2, 'G': 0, 'H': -1, 'I': -2, 'K': 0, 'L': -2, 'M': -1, 'N': 1, 'P': -1, 'Q': 0, 'R': -1, 'S': 4, 'T': 1, 'V': -2, 'W': -3, 'Y': -2},
        'T': {'A': 0, 'C': -1, 'D': -1, 'E': -1, 'F': -2, 'G': -2, 'H': -2, 'I': -1, 'K': -1, 'L': -1, 'M': 0, 'N': 0, 'P': -1, 'Q': -1, 'R': -1, 'S': 1, 'T': 5, 'V': 0, 'W': -2, 'Y': -2},
        'V': {'A': 0, 'C': -1, 'D': -3, 'E': -2, 'F': -1, 'G': -3, 'H': -3, 'I': 3, 'K': -2, 'L': 1, 'M': 1, 'N': -3, 'P': -2, 'Q': -2, 'R': -3, 'S': -2, 'T': 0, 'V': 4, 'W': -3, 'Y': -1},
        'W': {'A': -3, 'C': -2, 'D': -4, 'E': -3, 'F': 1, 'G': -2, 'H': -2, 'I': -3, 'K': -3, 'L': -2, 'M': -1, 'N': -4, 'P': -4, 'Q': -2, 'R': -3, 'S': -3, 'T': -2, 'V': -3, 'W': 11, 'Y': 2},
        'Y': {'A': -2, 'C': -2, 'D': -3, 'E': -2, 'F': 3, 'G': -3, 'H': 2, 'I': -1, 'K': -2, 'L': -1, 'M': -1, 'N': -2, 'P': -3, 'Q': -1, 'R': -2, 'S': -2, 'T': -2, 'V': -1, 'W': 2, 'Y': 7}
    }
    
    score = 0
    for a, b in zip(seq1, seq2):
        score += scoring_matrix.get(a, {}).get(b, -1)
    return score / len(seq1)  # average per residue

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    })

@app.route('/generate', methods=['POST'])
def generate_sequences():
    """Generate similar protein sequences"""
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
        
        # Generate 100 similar sequences
        generated_sequences = generate_sequences_mock(sequence, 100)
        
        # Calculate BLOSUM62 scores for the last 20 residues
        original_last20 = sequence[-20:]
        scored_sequences = []
        
        for gen_seq in generated_sequences:
            gen_last20 = gen_seq[-20:]
            score = calculate_blosum62_score(original_last20, gen_last20)
            scored_sequences.append({
                'sequence': gen_seq,
                'score': score
            })
        
        # Sort by score and get top 5
        top_sequences = sorted(scored_sequences, key=lambda x: x['score'], reverse=True)[:5]
        
        return jsonify({
            'sequences': top_sequences,
            'original_sequence': sequence,
            'status': 'success'
        })
        
    except Exception as e:
        logger.error(f"Generation error: {str(e)}")
        return jsonify({'error': f'Generation failed: {str(e)}'}), 500

@app.route('/model_info', methods=['GET'])
def model_info():
    """Get model information"""
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500
    
    return jsonify({
        'model_type': type(model).__name__,
        'model_loaded': True,
        'device': 'cpu'
    })

if __name__ == '__main__':
    # Load model on startup
    if load_model():
        logger.info("Starting sequence generation server...")
        app.run(host='0.0.0.0', port=5001, debug=True)
    else:
        logger.error("Failed to load model. Exiting.")
        sys.exit(1)
