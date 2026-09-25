import os
import numpy as np
from . import DetectedObject

INDIAN_ROAD_CLASSES = {
    0: 'auto_rickshaw',
    1: 'cow_cattle',
    2: 'pedestrian',
    3: 'two_wheeler',
    4: 'pothole',
    5: 'truck_bus',
    6: 'car'
}

class CameraDetector:
    """Camera Object Detector supporting YOLO models and synthetic high-fidelity sensor feeds."""
    def __init__(self, model_weights=None, conf_threshold=0.45):
        self.conf_threshold = conf_threshold
        self.model = None
        if model_weights and os.path.exists(model_weights):
            try:
                from ultralytics import YOLO
                self.model = YOLO(model_weights)
                print(f"[Perception] Loaded custom YOLO model: {model_weights}")
            except Exception as e:
                print(f"[Perception] Warning: Could not load YOLO weights ({e}), falling back to simulation mode.")

    def detect_frame(self, frame_or_sim_actors, ego_pose):
        """
        Detects objects in camera FOV.
        In simulation, models camera FOV angle (120 deg) and range (~60m).
        """
        detections = []
        if self.model and isinstance(frame_or_sim_actors, np.ndarray):
            results = self.model.predict(frame_or_sim_actors, conf=self.conf_threshold, verbose=False)
            for r in results:
                for box in r.boxes:
                    cls_id = int(box.cls[0])
                    conf = float(box.conf[0])
                    label = INDIAN_ROAD_CLASSES.get(cls_id, 'obstacle')
                    detections.append({'label': label, 'bbox': box.xyxy[0].tolist(), 'conf': conf})
            return detections

        # Simulation mode: filter ground-truth actors within camera FOV
        ego_x, ego_y, ego_yaw = ego_pose
        fov_rad = np.radians(120)
        max_camera_range = 60.0

        for actor in frame_or_sim_actors:
            dx = actor['x'] - ego_x
            dy = actor['y'] - ego_y
            dist = np.hypot(dx, dy)

            # Check distance limit
            if dist > max_camera_range:
                continue

            # Angle relative to ego heading
            angle_to_actor = np.arctan2(dy, dx) - ego_yaw
            angle_to_actor = (angle_to_actor + np.pi) % (2 * np.pi) - np.pi

            if abs(angle_to_actor) <= (fov_rad / 2):
                # Add realistic sensor noise (Gaussian)
                noise_x = np.random.normal(0, 0.15)
                noise_y = np.random.normal(0, 0.15)
                detected = DetectedObject(
                    obj_id=actor['id'],
                    class_name=actor['class'],
                    x=actor['x'] + noise_x,
                    y=actor['y'] + noise_y,
                    vx=actor.get('vx', 0.0),
                    vy=actor.get('vy', 0.0),
                    width=actor.get('width', 1.5),
                    length=actor.get('length', 3.0),
                    confidence=np.clip(np.random.normal(0.92, 0.04), 0.70, 0.99)
                )
                detections.append(detected)

        return detections
