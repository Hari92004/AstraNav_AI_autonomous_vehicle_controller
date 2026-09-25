# 📘 AI Model Training Guide (SIH 2026)

## 📁 Required Models Overview:
1. **Model 1 (2D Camera YOLOv8):** Indian Traffic Object Detector (`auto_rickshaw`, `cow_cattle`, `pedestrian`, `two_wheeler`, `pothole`, `truck_bus`, `car`).
2. **Model 2 (Multi-Agent Trajectory Predictor):** Non-lane future motion forecaster (1.0 to 3.0 seconds horizon).

---

## 🛠️ Step 1: Dataset Setup

1. **Download Indian Driving Dataset (IDD) & Cattle Dataset:**
   - **IDD Dataset:** [idd.insaan.iiit.ac.in](https://idd.insaan.iiit.ac.in/)
   - **Roboflow Indian Cattle:** [universe.roboflow.com](https://universe.roboflow.com/search?q=indian+cattle)
2. **Folder Structure Setup:**
   Apne PC me images aur labels is structure me rakhein:
   ```
   d:/SIH2026/datasets/indian_traffic/
   ├── images/
   │   ├── train/     # Training images (.jpg / .png)
   │   └── val/       # Validation images (.jpg / .png)
   └── labels/
       ├── train/     # YOLO format .txt annotations
       └── val/       # YOLO format .txt annotations
   ```

---

## 🚀 Step 2: Training YOLOv8 (Camera Vision Model)

Terminal kholiye aur command run kijiye:

```bash
cd d:\SIH2026\training_suite
python train_yolo_detector.py
```

### 🎯 Training Output:
- **`sih2026_runs/yolov8_indian_traffic/weights/best.pt`**: Best PyTorch weights.
- **`sih2026_runs/yolov8_indian_traffic/weights/best.onnx`**: MATLAB-compatible model.
- **Metrics:** mAP@0.50, Precision, Recall graphs.

---

## 🚀 Step 3: Training Trajectory Predictor (Motion Forecasting Model)

Terminal me command run kijiye:

```bash
cd d:\SIH2026\training_suite
python train_trajectory_predictor.py
```

### 🎯 Training Output:
- **`trajectory_model.pth`**: Trained PyTorch weights.
- **`trajectory_predictor.onnx`**: Ready for MATLAB Deep Learning Toolbox.

---

## 🔄 Step 4: MATLAB Me Trained Models Load Karna

MATLAB Command Window me aap in models ko directly load kar sakte hain:

```matlab
% 1. Load Trained YOLO Detector into MATLAB
net_yolo = importONNXNetwork('d:/SIH2026/training_suite/best.onnx');

% 2. Load Trajectory Predictor into MATLAB
net_pred = importONNXNetwork('d:/SIH2026/training_suite/trajectory_predictor.onnx');
```
