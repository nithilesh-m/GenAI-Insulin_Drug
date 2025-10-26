@echo off
echo Starting Protein Sequence Generator Backend...
echo.
echo Make sure you have Python installed and the final_ckpt.pt file in the root directory.
echo.
cd backend
python sequence_server.py
pause
