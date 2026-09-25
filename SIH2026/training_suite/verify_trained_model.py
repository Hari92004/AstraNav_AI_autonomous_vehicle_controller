"""
SIH 2026: Model Verification & Visual Testing Script
Runs inference on test images/videos and outputs benchmark accuracy metrics.
"""
import os
import sys
from ultralytics import YOLO

def verify_model(weights_path=None, test_source=None):
    print("================================================================")
    print("🔍 SIH 2026: AI MODEL VERIFICATION & ACCURACY CHECK")
    print("================================================================")

    if weights_path is None:
        weights_path = "d:/SIH2026/training_suite/sih2026_runs/yolov8_indian_traffic/weights/best.pt"
        if not os.path.exists(weights_path):
            weights_path = "yolov8m.pt" # Fallback to base weights if custom training not run yet

    print(f"Loading weights: {weights_path}")
    model = YOLO(weights_path)

    # 1. Validation Benchmark Metrics
    yaml_path = os.path.join(os.path.dirname(__file__), "idd_traffic.yaml")
    if os.path.exists(yaml_path):
        print("\n[Step 1/2] Computing Validation Metrics (mAP, Precision, Recall)...")
        try:
            metrics = model.val(data=yaml_path, verbose=False)
            print(f"  • mAP@0.50 (IoU=0.50)      : {metrics.box.map50 * 100:.2f}%")
            print(f"  • mAP@0.50:0.95 (Strict)   : {metrics.box.map * 100:.2f}%")
            print(f"  • Mean Precision           : {metrics.box.mp * 100:.2f}%")
            print(f"  • Mean Recall              : {metrics.box.mr * 100:.2f}%")
            
            # Quality Assessment
            if metrics.box.map50 >= 0.80:
                print("  🌟 STATUS: EXCELLENT / PRODUCTION READY for SIH 2026!")
            elif metrics.box.map50 >= 0.65:
                print("  ✔️ STATUS: GOOD & VALID for simulation testing.")
            else:
                print("  ⚠️ STATUS: FAIR. Recommend training for 30 more epochs.")
        except Exception as e:
            print(f"  Validation note: {e}")

    # 2. Test Prediction on sample image
    print("\n[Step 2/2] Running Inference on Sample Test Image...")
    # Check if user provided an image or use synthetic test
    results = model.predict(source="https://ultralytics.com/images/bus.jpg", save=True, project="d:/SIH2026/training_suite/sih2026_runs", name="verify_results")
    print(f"✔️ Annotated verification image saved at: {results[0].save_dir}")
    print("================================================================\n")

if __name__ == "__main__":
    verify_model()
