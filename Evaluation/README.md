# SIH 2026: Evaluation & Benchmarking Suite
**Problem Statement ID:** 26037 (AI Perception, Sensor Fusion & Trajectory Prediction)  
**Location:** `D:\SIH26\Evaluation`

This folder contains the complete verification, testing, and automated evaluation pipeline for all **3 Core AI Models** built for Indian autonomous driving.

---

## 📁 Files in This Directory

- **`evaluate_all_models.py`**: The unified Python benchmark script. It loads each model (Camera YOLO, 3D LiDAR, Trajectory Predictor), runs inference on validation datasets, measures latency/FPS, and computes standard ADAS metrics.
- **`run_evaluation.bat`**: 1-click Windows batch runner. Double-click this file from File Explorer to automatically run the evaluation and update results.
- **`EVALUATION_REPORT.md`**: Generated markdown report containing full performance tables, precision/recall, 3D translation errors, and displacement errors.
- **`metrics_summary.json`**: Machine-readable JSON summary of all benchmarks for dashboard integration or MATLAB ingestion.

---

## ⚡ How to Run Evaluation

### Method 1: 1-Click Batch Runner
Double-click `run_evaluation.bat` in File Explorer, or run in Command Prompt / PowerShell:
```cmd
cd D:\SIH26\Evaluation
run_evaluation.bat
```

### Method 2: Python Terminal
```bash
cd D:\SIH26\Evaluation
python evaluate_all_models.py
```

---

## 📊 Summary of Evaluated Metrics

| Model | Architecture | Primary Accuracy Metric | Benchmark Target | Achieved Result | Latency / FPS |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Model 1 (2D Camera)** | Spatial-Grid YOLO | **Classification Accuracy** | > 90.0% | **95.80%** (Precision: 94.2%, Recall: 92.5%) | 9.85 ms (101.5 FPS) |
| **Model 2 (3D LiDAR)** | PointPillars 3D Net | **Average Translation Error (ATE)** | < 0.50 m | **0.450 m** (3D Box Error: 0.367 m) | 7.91 ms (126.5 FPS) |
| **Model 3 (Trajectory)** | Temporal 1D Conv Net | **Average Disp. Error (ADE)** | < 0.50 m | **0.408 m** (FDE @ 2.4s: 0.914 m) | 0.42 ms (2379 FPS) |

---

## 🎯 Validation Dataset Sources

1. **Model 1**: 30 validation frames with 7-class Indian traffic labels (`D:\SIH26\Model1\dataset\images\val`).
2. **Model 2**: 404 keyframes from nuScenes 32-beam LiDAR binary point clouds (`D:\SIH26\dataset mini\v1.0-mini`).
3. **Model 3**: 500 validation motion trajectories of Indian vehicles, cattle, and pedestrians (`D:\SIH26\model3`).
