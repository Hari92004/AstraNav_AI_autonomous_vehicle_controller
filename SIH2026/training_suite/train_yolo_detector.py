"""
SIH 2026: Custom YOLOv8 Training Script for Indian Road Traffic
Trains on IDD + Roboflow Cattle/Pothole dataset and exports to MATLAB ONNX.
"""
import os
import sys
import torch
from ultralytics import YOLO

def train_custom_yolo():
    print("================================================================")
    print("🚀 SIH 2026: STARTING CUSTOM YOLOV8 TRAINING (INDIAN TRAFFIC)")
    print("================================================================")

    # 1. Check GPU / CUDA Availability
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        gpu_vram = torch.cuda.get_device_properties(0).total_memory / (1024**3)
        print(f"✔️ GPU Detected: {gpu_name} ({gpu_vram:.1f} GB VRAM)")
        device = 0
    else:
        print("⚠️ No GPU detected, running on CPU (will be slower).")
        device = 'cpu'

    # 2. Load Pretrained Base Weights (Transfer Learning)
    # yolov8m (medium) gives the ideal balance of accuracy and high FPS
    print("\n[Step 1/4] Loading pretrained YOLOv8m base weights...")
    model = YOLO("yolov8m.pt")

    # 3. Start Training
    yaml_path = os.path.join(os.path.dirname(__file__), "idd_traffic.yaml")
    print(f"\n[Step 2/4] Starting training with config: {yaml_path}")
    print("Hyperparameters: epochs=50, imgsz=640, batch=16, optimizer=AdamW")

    try:
        results = model.train(
            data=yaml_path,
            epochs=50,             # 50 epochs is standard for fine-tuning
            imgsz=640,            # Standard high resolution
            batch=16,             # Adjust to 8 or 32 based on GPU VRAM
            device=device,
            workers=4,
            optimizer="AdamW",
            lr0=0.001,            # Initial learning rate
            lrf=0.01,             # Final learning rate
            augment=True,         # Auto data augmentation (blur, mosaic, flip)
            project="sih2026_runs",
            name="yolov8_indian_traffic",
            save=True,
            val=True
        )
        print("\n✔️ Training successfully completed!")

    except Exception as e:
        print(f"\n⚠️ Note during training setup: {e}")
        print("If dataset folder is not yet populated, please place your dataset in ./datasets/indian_traffic")
        return

    # 4. Evaluate on Validation Set
    print("\n[Step 3/4] Evaluating Model Metrics on Validation Set...")
    metrics = model.val()
    print(f"• mAP@0.50     : {metrics.box.map50:.4f}")
    print(f"• mAP@0.50:0.95: {metrics.box.map:.4f}")

    # 5. Export to ONNX for MATLAB Integration
    print("\n[Step 4/4] Exporting model to ONNX format for MATLAB...")
    onnx_path = model.export(format="onnx", opset=12, dynamic=False)
    print(f"✔️ MATLAB ONNX Model saved at: {onnx_path}")
    print("\n🎉 You can now load this in MATLAB using: importONNXNetwork('best.onnx')")

if __name__ == "__main__":
    train_custom_yolo()
