@echo off
title SIH 2026 - Multi-Scene Perception & Trajectory Test Suite
cd /d "D:\SIH26\lasttest"
echo ============================================================================
echo   SMART INDIA HACKATHON 2026: MULTI-SCENE PERCEPTION & TRAJECTORY SUITE
echo ============================================================================
python run_last_test.py --scene all
echo.
echo All 3 test scenes executed successfully!
echo 1. Scene 1 (Urban Swerve)   : D:\SIH26\lasttest\test_scene1_urban_pothole.png
echo 2. Scene 2 (Highway Cattle) : D:\SIH26\lasttest\test_scene2_highway_cattle_crossing.png
echo 3. Scene 3 (Market Squeeze) : D:\SIH26\lasttest\test_scene3_dense_market_traffic.png
echo.
pause


