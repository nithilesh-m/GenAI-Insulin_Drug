@echo off
echo Starting Protein to SMILES Predictor Backend...
echo.
echo Make sure you have Python installed and the fusion_best.pt file in the root directory.
echo.
cd backend
python model_server.py
pause
