# Protein AI Tools

A React-based web application with two powerful protein analysis tools:

1. **SMILES Predictor**: Predicts drug SMILES structures from 50-character mutated protein sequences
2. **Sequence Generator**: Generates similar mutated protein sequences with BLOSUM62 scoring

## Features

### SMILES Predictor
- 🧬 **Protein Sequence Input**: Enter exactly 50 amino acid characters
- 🤖 **AI Prediction**: Uses a trained PyTorch model to predict drug SMILES
- 🎨 **Beautiful UI**: Modern, responsive design with gradient themes
- 📱 **Mobile Friendly**: Fully responsive across all devices
- ⚡ **Real-time Validation**: Input validation with character counting
- 📋 **Copy to Clipboard**: Easy copying of predicted SMILES structures

### Sequence Generator
- 🧬 **Protein Sequence Input**: Enter exactly 50 amino acid characters
- 🔄 **Sequence Generation**: Generates 100 similar sequences using AI model
- 📊 **BLOSUM62 Scoring**: Ranks sequences by similarity using BLOSUM62 matrix
- 🏆 **Top 5 Results**: Shows the 5 most similar sequences with scores
- 📋 **Copy Sequences**: Easy copying of individual sequences

## Project Structure

```
├── src/
│   ├── App.js                    # Main React component with navigation
│   ├── SMILESPredictor.js        # SMILES prediction component
│   ├── SequenceGenerator.js      # Sequence generation component
│   ├── index.js                  # React entry point
│   ├── styles.css                # CSS styles
│   └── utils/
│       ├── modelUtils.js         # SMILES prediction utilities
│       └── sequenceUtils.js      # Sequence generation utilities
├── backend/
│   ├── model_server.py           # Flask backend for SMILES prediction
│   ├── sequence_server.py        # Flask backend for sequence generation
│   └── requirements.txt          # Python dependencies
├── public/
│   └── index.html                # HTML template
├── fusion_best.pt                # SMILES prediction model
├── final_ckpt.pt                 # Sequence generation model
├── package.json                  # Node.js dependencies
├── webpack.config.js             # Webpack configuration
└── README.md                     # This file
```

## Setup Instructions

### Prerequisites

- Node.js (v14 or higher)
- Python 3.7 or higher
- pip (Python package manager)

### Frontend Setup

1. **Install Node.js dependencies:**
   ```bash
   npm install
   ```

2. **Start the development server:**
   ```bash
   npm start
   ```

3. **Open your browser:**
   Navigate to `http://localhost:3000`

### Backend Setup (Optional)

The app works with mock predictions by default. To use your actual PyTorch model:

1. **Install Python dependencies:**
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. **Start the model server:**
   ```bash
   python model_server.py
   ```

3. **The backend will run on:** `http://localhost:5000`

## Usage

1. **Enter Protein Sequence**: Type exactly 50 amino acid characters (A, C, D, E, F, G, H, I, K, L, M, N, P, Q, R, S, T, V, W, Y)

2. **Click Predict**: The app will process your sequence and generate a drug SMILES structure

3. **Copy Results**: Use the "Copy SMILES" button to copy the predicted structure to your clipboard

## Model Integration

The app supports two modes:

### Mock Mode (Default)
- Works without any backend
- Generates realistic-looking SMILES for demonstration
- Perfect for testing the UI and functionality

### Real Model Mode
- Requires the backend server running
- Uses your actual `fusion_best.pt` PyTorch model
- Provides real predictions based on your trained model

## Customization

### Styling
- Edit `src/styles.css` to modify colors, fonts, and layout
- The app uses a modern gradient theme that can be easily customized

### Model Integration
- Modify `backend/model_server.py` to adjust model preprocessing/postprocessing
- Update `src/utils/modelUtils.js` to change API endpoints or add new features

## Technical Details

- **Frontend**: React 18 with modern hooks
- **Styling**: Custom CSS with responsive design
- **Build Tool**: Webpack 5 with Babel
- **Backend**: Flask with PyTorch
- **Model Format**: PyTorch .pt files

## Troubleshooting

### Common Issues

1. **"Backend not available" message**: This is normal if you're not running the Python backend. The app will use mock predictions.

2. **Model loading errors**: Ensure your `fusion_best.pt` file is in the project root directory.

3. **Port conflicts**: If ports 3000 or 5000 are in use, modify the configuration files to use different ports.

### Development Tips

- Use browser developer tools to see console logs
- Check the Network tab to monitor API calls
- The app gracefully falls back to mock predictions if the backend is unavailable

## License

MIT License - feel free to use and modify as needed.

## Support

For issues or questions, please check the console logs and ensure all dependencies are properly installed.
