# SIH 2026: Laptop 2 (MATLAB / Simulink) Deployment Package
**Problem Statement ID:** 26037 (Autonomous Navigation in Unstructured Indian Road Traffic)  
**Package Folder:** `D:\SIH26\LAPTOP2_DEPLOYMENT`

---

## 📦 What is Inside This Folder

This folder is a standalone, self-contained deployment bundle ready to copy to **Laptop 2 (Simulation Machine)**:

| File Name | Description | Size |
| :--- | :--- | :--- |
| **`model1_camera_yolo.onnx`** | 2D Camera Vision YOLO Network (7 Indian road classes) | **4.52 MB** |
| **`model2_lidar.onnx`** | 3D LiDAR PointPillars Detector (16,384 points input) | **2.26 MB** |
| **`model3_trajectory_predictor.onnx`** | Indian Traffic Trajectory Predictor (2.4s future forecast) | **1.44 MB** |
| **`test_models_in_matlab.m`** | Ready-to-run MATLAB test script (loads all 3 models & verifies inference) | 4.8 KB |
| **`simulink_perception_block.m`** | Ready-to-paste MATLAB Function Block for your Simulink model | 2.1 KB |
| **`test_models_in_python.py`** | Standalone Python ONNX tester (for fast command-line testing) | 2.8 KB |
| **`test_camera_frame.jpg`** | Sample photorealistic Indian road camera frame | 1.01 MB |
| **`test_lidar_pointcloud.npy`** | Sample 32-beam Velodyne LiDAR point cloud | 262 KB |

---

## 🚀 Step-by-Step Instructions for Laptop 2

### Step 1: Transfer the Folder to Laptop 2
1. Copy the entire **`LAPTOP2_DEPLOYMENT`** folder to a USB Pen Drive or via local WiFi / Ethernet share.
2. Paste it on Laptop 2 (e.g., `C:\SIH2026\LAPTOP2_DEPLOYMENT\` or on Desktop).

---

### Step 2: Test in MATLAB (Command Window / Editor)
1. Open **MATLAB** on Laptop 2.
2. In the MATLAB Current Folder bar, navigate to the `LAPTOP2_DEPLOYMENT` folder.
3. Open **`test_models_in_matlab.m`** and click **Run** (or type `test_models_in_matlab` in the Command Window).
4. MATLAB will:
   - Load `model1_camera_yolo.onnx` with `importONNXNetwork` and detect the 7 classes.
   - Load `model2_lidar.onnx` and regress 3D bounding boxes.
   - Load `model3_trajectory_predictor.onnx` and forecast 12 future timesteps (2.4s).
   - Display latency and verify compliance with the 50 Hz MathWorks control loop budget (< 20 ms).

---

### Step 3: Integrate with Your Simulink Model
1. In your Simulink model, add a **MATLAB Function** block inside your Perception Subsystem.
2. Copy the contents of **`simulink_perception_block.m`** and paste them into the block editor.
3. Connect your simulation sensor signals:
   - Connect Camera RGB image (`[640 x 640 x 3] uint8`) to input `camRGB`.
   - Connect Simulation LiDAR point cloud (`[16384 x 4] single`) to input `lidarPts`.
   - Connect Kalman tracker obstacle histories (`[N x 8 x 2] single`) to input `pastTracks`.
4. Connect the block outputs:
   - Output `detectedBoxes` $\to$ Visual Bounding Box Overlay.
   - Output `lidar3DBoxes` $\to$ Sensor Fusion / World Coordinate Mapper.
   - Output `futurePaths` $\to$ Frenet Local Path Planner & Collision Avoidance Block!

---

### Step 4 (Optional): Quick Standalone Test in Python
On Laptop 2, you can also test without opening MATLAB:
```bash
python test_models_in_python.py
```
This tests all 3 models in less than 2 seconds!
