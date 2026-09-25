# End-to-End Multi-Sensor Perception & Trajectory Visualizer
**Location:** `D:\SIH26\Evaluation\lasttest`

This folder contains the complete live test combining **Model 1 (2D Camera Vision)**, **Model 2 (3D LiDAR Point Cloud)**, and **Model 3 (Indian Trajectory Prediction)** into an integrated visual pipeline with ego-vehicle collision avoidance path planning.

---

## 📁 Files in This Directory

- **`run_last_test.py`**: Python script that loads synchronized camera and LiDAR frames, executes predictions across all models, predicts future trajectories (2.4s horizon), plans an avoidance path, and renders the composite visualization image.
- **`run_test.bat`**: 1-click Windows batch runner. Double-click to execute and generate images.
- **`end_to_end_perception_result.png`**: High-resolution composite visual image containing:
  - **Panel 1**: 2D Camera image with detected bounding boxes, class labels, and confidence percentages.
  - **Panel 2**: 3D LiDAR Bird's-Eye-View (BEV) with point clouds, 3D oriented obstacle boxes, Model 3 trajectory forecasts (12 steps / 2.4 seconds), and green Frenet collision-free avoidance path.
  - **Telemetry HUD**: Ego speed, steering angle, frame rates (FPS), and controller compliance status.
- **`LAST_TEST_REPORT.md`**: Markdown summary detailing obstacle positions, predictions, and latencies.

---

## ⚡ How to Run

Double-click `run_test.bat` or run in terminal:
```bash
cd D:\SIH26\Evaluation\lasttest
python run_last_test.py
```
