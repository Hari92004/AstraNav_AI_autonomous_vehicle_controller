# 🚀 SIH 2026: 3 AI Models Demo Training Suite (VS Code)

This demo suite lets you generate synthetic Indian road data, train **all 3 required AI models**, evaluate their metrics, and export them into **MATLAB-compatible `.onnx` files** in under 3 minutes!

---

## 📁 Files in this Suite:
- **`00_generate_dummy_dataset.py`**: Creates synthetic images, YOLO labels (.txt), and 3D LiDAR point clouds (.bin).
- **`01_train_camera_yolo.py`**: Trains Model 1 (2D Camera YOLOv8) on Indian traffic classes.
- **`02_train_lidar_detector.py`**: Trains Model 2 (3D LiDAR Point Cloud Detector).
- **`03_train_trajectory_predictor.py`**: Trains Model 3 (Multi-Agent Seq2Seq GRU Trajectory Predictor).
- **`run_all_demo_training.py`**: 1-Click Master Runner that executes everything automatically.

---

## ⚡ How to Run in VS Code (2 Simple Steps):

### Step 1: Open Terminal in VS Code
Press ``Ctrl + ` `` to open the VS Code Terminal and navigate to this folder:
```bash
cd d:\SIH2026\demo_training_suite
```

### Step 2: Run the 1-Click Master Runner
```bash
python run_all_demo_training.py
```

---

## 🎯 What Happens Automatically:
1. **Synthetic Dataset Generation:** Creates 50 Indian road images (with Auto-rickshaws, Cows, Pedestrians, Potholes) and 10 LiDAR point cloud files in `datasets/indian_traffic_dummy/`.
2. **Model 1 Training (YOLOv8):** Runs 5 fast epochs, detects classes, and exports `best.onnx`.
3. **Model 2 Training (3D LiDAR):** Trains a PointNet 3D bounding-box regressor and exports `lidar_3d_detector.onnx`.
4. **Model 3 Training (Trajectory Predictor):** Trains a Seq2Seq GRU on non-lane motion curves and exports `trajectory_predictor.onnx`.

---

## 🔄 MATLAB Direct Integration:
In MATLAB Command Window, you can load these models directly:
```matlab
% 1. Load Camera YOLOv8 Detector
net_camera = importONNXNetwork('d:/SIH2026/demo_training_suite/runs_yolo/demo_yolo_model/weights/best.onnx');

% 2. Load 3D LiDAR Detector
net_lidar = importONNXNetwork('d:/SIH2026/demo_training_suite/lidar_3d_detector.onnx');

% 3. Load Trajectory Predictor
net_trajectory = importONNXNetwork('d:/SIH2026/demo_training_suite/trajectory_predictor.onnx');
```
