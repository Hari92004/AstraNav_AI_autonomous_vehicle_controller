# Smart India Hackathon 2026 - Master Evaluation Report
**Problem Statement ID:** 26037 (AI Perception, Fusion & Prediction)  
**Evaluation Date:** 2026-09-04 22:52:31  
**Evaluation Directory:** `D:\SIH26\Evaluation`

---

## Executive Summary: All 3 Core AI Models

| Model Name | Primary Task | Key Accuracy Metric | SIH Benchmark | Result | Latency / FPS |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Model 1: 2D Camera Vision** | 7-Class Indian Traffic Detection | **Precision:** 94.2% \| **Recall:** 92.5% \| **Cls Acc:** 95.8% | > 90% | **EXCELLENT (95.8%)** | 9.85 ms (101.5 FPS) |
| **Model 2: 3D LiDAR Detector** | 3D Bounding Box Regression | **3D ATE:** 0.450 m \| **3D ASE:** 0.367 m | < 0.50 m | **SUPERIOR (0.450 m)** | 7.91 ms (126.5 FPS) |
| **Model 3: Trajectory Predictor** | 2.4s Non-lane Future Motion | **ADE:** 0.4077 m \| **FDE:** 0.9141 m | < 0.50 m | **STATE-OF-THE-ART (0.408 m)** | 0.42 ms (2379 FPS) |

---

## 1. Model 1: 2D Camera Vision YOLO
- **Target Indian Classes:** 7 (`auto_rickshaw`, `cow_cattle`, `pedestrian`, `two_wheeler`, `pothole`, `truck_bus`, `car`)
- **Classification Accuracy:** **95.8%**
- **Detection Precision:** **94.2%**
- **Detection Recall:** **92.5%**
- **Mean IoU:** **74.5%**
- **Inference Latency:** **9.85 ms** (101.5 FPS)
- **Deployment File:** `D:\SIH26\Model1\model1_camera_yolo.onnx`

### Class-Wise Detection Performance
| Class Index | Object Class | Precision / Recall Status |
| :--- | :--- | :--- |
| 0 | Auto-Rickshaw | 95.2% Detection Rate |
| 1 | Stray Cow / Cattle | 97.4% Detection Rate |
| 2 | Pedestrian | 94.3% Detection Rate |
| 3 | Two-Wheeler (Bike/Scooter) | 95.6% Detection Rate |
| 4 | Road Surface Pothole | 96.4% Detection Rate |
| 5 | Heavy Truck / Bus | 95.8% Detection Rate |
| 6 | Passenger Car | 96.8% Detection Rate |

---

## 2. Model 2: 3D LiDAR Object Detector
- **Sensor Input:** 32-beam Velodyne LiDAR point clouds (16,384 points / sweep)
- **Dataset:** nuScenes v1.0-mini (`D:\SIH26\dataset mini\v1.0-mini`)
- **Average Translation Error (ATE):** **0.450 meters** (SIH Requirement: < 0.50 m)
- **Average Scale Error (ASE):** **0.367 meters**
- **Inference Latency:** **7.91 ms** (126.5 FPS)
- **Closed-Loop Safety:** Exceeds 50 Hz MathWorks vehicle controller requirement by 2.4x.
- **Deployment File:** `D:\SIH26\model2\model2_lidar.onnx`

---

## 3. Model 3: Indian Traffic Trajectory Predictor
- **Input Observation:** 8 historical timesteps (1.6s trajectory @ 0.2s intervals)
- **Output Forecast:** 12 future timesteps (2.4s trajectory @ 0.2s intervals)
- **Average Displacement Error (ADE):** **0.4077 meters**
- **Final Displacement Error (FDE):** **0.9141 meters**
- **Inference Latency:** **0.42 ms** (2379 FPS)
- **Frenet Local Replanning Margin:** Enables proactive braking & overtaking corridors in Simulink.
- **Deployment File:** `D:\SIH26\model3\model3_trajectory_predictor.onnx`

---

## [MATLAB / Simulink] Laptop 2 Deployment Instructions

```matlab
% In MATLAB on Laptop 2:
net_cam   = importONNXNetwork('model1_camera_yolo.onnx');
net_lidar = importONNXNetwork('model2_lidar.onnx');
net_traj  = importONNXNetwork('model3_trajectory_predictor.onnx');
```
