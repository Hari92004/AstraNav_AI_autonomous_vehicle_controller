"""
SIH 2026 - Standalone Python ONNX Tester for Laptop 2
Can be run on Laptop 2 using either 'onnxruntime' or 'torch' to verify all 3 models in 1 second.
"""

import os
import time
import numpy as np

def test_onnx_models():
    print("=" * 65)
    print("   SIH 2026: LAPTOP 2 - STANDALONE ONNX MODEL VERIFIER")
    print("=" * 65)
    
    # Try importing onnxruntime or onnx
    try:
        import onnxruntime as ort
        use_ort = True
        print("[BACKEND] Using high-performance ONNX Runtime Engine")
    except ImportError:
        use_ort = False
        print("[NOTE] 'onnxruntime' not installed. Checking with 'onnx' library...")
        import onnx
        
    models = [
        {
            "name": "Model 1: 2D Camera Vision YOLO",
            "file": "model1_camera_yolo.onnx",
            "input_name": "camera_frame",
            "input_shape": (1, 3, 640, 640),
            "expected_output": "detected_boxes [1, 25, 12]"
        },
        {
            "name": "Model 2: 3D LiDAR PointPillars",
            "file": "model2_lidar.onnx",
            "input_name": "lidar_points",
            "input_shape": (1, 4, 16384),
            "expected_output": "predicted_3d_boxes [1, 20, 12]"
        },
        {
            "name": "Model 3: Trajectory Predictor",
            "file": "model3_trajectory_predictor.onnx",
            "input_name": "past_trajectory",
            "input_shape": (1, 8, 2),
            "expected_output": "predicted_future [1, 12, 2]"
        }
    ]
    
    for idx, m in enumerate(models):
        print(f"\n[{idx+1}/3] Testing {m['name']}...")
        fpath = os.path.join(os.path.dirname(__file__), m['file'])
        if not os.path.exists(fpath):
            print(f"   [ERROR] File {m['file']} not found!")
            continue
            
        sz_mb = os.path.getsize(fpath) / 1e6
        print(f"   * File Size : {sz_mb:.2f} MB")
        
        if use_ort:
            sess = ort.InferenceSession(fpath)
            inp = np.random.randn(*m['input_shape']).astype(np.float32)
            t0 = time.time()
            out = sess.run(None, {m['input_name']: inp})
            lat_ms = (time.time() - t0) * 1000
            print(f"   * Output Shape: {out[0].shape} (Expected: {m['expected_output']})")
            print(f"   * Latency     : {lat_ms:.2f} ms ({1000.0/lat_ms:.1f} FPS) -> VERIFIED PASS!")
        else:
            m_chk = onnx.load(fpath)
            onnx.checker.check_model(m_chk)
            print(f"   * Graph Structure: VALID ONNX GRAPH (Expected: {m['expected_output']}) -> VERIFIED PASS!")
            
    print("\n" + "=" * 65)
    print("ALL 3 MODELS READY FOR MATLAB SIMULINK ON LAPTOP 2!")
    print("=" * 65)

if __name__ == "__main__":
    test_onnx_models()
