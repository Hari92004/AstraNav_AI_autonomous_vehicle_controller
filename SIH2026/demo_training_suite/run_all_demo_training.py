"""
SIH 2026: Master Demo Training Suite Runner
Executes Dummy Data Generation -> Model 1 (YOLO) -> Model 2 (LiDAR) -> Model 3 (Trajectory Prediction)
"""
import os
import sys
import time

def run_master_demo_suite():
    print("\n" + "=" * 70)
    print("🚀 SIH 2026: 1-CLICK MASTER DEMO TRAINING SUITE (3 AI MODELS)")
    print("=" * 70 + "\n")

    t_start = time.time()

    # Step 1: Generate Synthetic Dataset
    print("[1/4] Running Dummy Dataset Generation...")
    import subprocess
    subprocess.run([sys.executable, "d:/SIH2026/demo_training_suite/00_generate_dummy_dataset.py"], check=True)

    # Step 2: Train Model 1 (YOLOv8)
    print("\n[2/4] Training Model 1 (2D Camera YOLOv8)...")
    from demo_training_suite.train_camera_yolo import run_camera_yolo_demo_training
    # Alternatively run via script
    subprocess.run([sys.executable, "d:/SIH2026/demo_training_suite/01_train_camera_yolo.py"], check=True)

    # Step 3: Train Model 2 (3D LiDAR Detector)
    print("\n[3/4] Training Model 2 (3D LiDAR Point Cloud Detector)...")
    subprocess.run([sys.executable, "d:/SIH2026/demo_training_suite/02_train_lidar_detector.py"], check=True)

    # Step 4: Train Model 3 (Trajectory Predictor)
    print("\n[4/4] Training Model 3 (Multi-Agent Trajectory Predictor)...")
    subprocess.run([sys.executable, "d:/SIH2026/demo_training_suite/03_train_trajectory_predictor.py"], check=True)

    elapsed = time.time() - t_start

    print("\n" + "=" * 70)
    print("🎉 ALL 3 AI MODELS SUCCESSFULLY TRAINED & EXPORTED TO ONNX!")
    print(f"⏱️ Total Execution Time: {elapsed:.1f} seconds")
    print("=" * 70)
    print("📁 Generated MATLAB-Ready ONNX Models:")
    print("  1. Camera 2D Model   : d:/SIH2026/demo_training_suite/runs_yolo/demo_yolo_model/weights/best.onnx")
    print("  2. LiDAR 3D Model    : d:/SIH2026/demo_training_suite/lidar_3d_detector.onnx")
    print("  3. Trajectory Model  : d:/SIH2026/demo_training_suite/trajectory_predictor.onnx")
    print("\n💡 MATLAB Load Syntax:")
    print("  net1 = importONNXNetwork('d:/SIH2026/demo_training_suite/runs_yolo/demo_yolo_model/weights/best.onnx');")
    print("  net2 = importONNXNetwork('d:/SIH2026/demo_training_suite/lidar_3d_detector.onnx');")
    print("  net3 = importONNXNetwork('d:/SIH2026/demo_training_suite/trajectory_predictor.onnx');")
    print("=" * 70 + "\n")

if __name__ == "__main__":
    run_master_demo_suite()
