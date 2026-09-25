@echo off
title SIH 2026 - Master Evaluation Suite
cd /d "D:\SIH26\Evaluation"
echo =======================================================================
echo     SMART INDIA HACKATHON 2026 - EVALUATING ALL 3 CORE AI MODELS
echo =======================================================================
python evaluate_all_models.py
echo.
echo Evaluation complete! Report generated in D:\SIH26\Evaluation\EVALUATION_REPORT.md
pause
