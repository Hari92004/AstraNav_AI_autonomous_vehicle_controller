"""
SIH 2026: Model 1 - 2D Vision YOLOv8 Demo Training Script
"""
import os
import torch
from ultralytics import YOLO

def run_camera_yolo_demo_training():
    print("================================================================")
    print("🧠 MODEL 1: TRAINING 2D VISION OBJECT DETECTOR (YOLOV8)")
    print("================================================================")

    # 1. Device check
    device = 0 if torch.cuda.is_available() else 'cpu'
    print(f"Executing on: {device} (CUDA={torch.cuda.is_available()})")

    # 2. Base model
    model = YOLO("yolov8n.pt") # Use nano for ultra-fast demo training

    # 3. Train on dummy dataset
    yaml_config = "d:/SIH2026/demo_training_suite/idd_dummy_config.yaml"
    print(f"Training on dummy Indian road data (5 epochs demo)...")

    results = model.train(
        data=yaml_config,
        epochs=5,
        imgsz=640,
        batch=8,
        device=device,
        project="d:/SIH2026/demo_training_suite/runs_yolo",
        name="demo_yolo_model",
        save=True,
        verbose=True
    )

    # 4. Export to ONNX for MATLAB
    print("\nExporting trained Model 1 to ONNX for MATLAB...")
    onnx_file = model.export(format="onnx", opset=12)
    print(f"✔️ Model 1 ONNX Exported: {onnx_file}")
    print("================================================================\n")

if __name__ == "__main__":
    run_camera_yolo_demo_training()
