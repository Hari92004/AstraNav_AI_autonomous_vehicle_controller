import numpy as np
from . import DetectedObject

class SensorFusionEngine:
    """
    Sensor Fusion Module: Combines Vision (Rich Semantic Classification) 
    and LiDAR (High Precision 3D Spatial Geometry).
    """
    def __init__(self, association_threshold=2.5):
        self.association_threshold = association_threshold

    def fuse(self, camera_objects, lidar_objects):
        """
        Fuses camera and LiDAR observations using spatial proximity association.
        """
        fused_objects = []
        matched_lidar_ids = set()

        for cam_obj in camera_objects:
            best_lidar = None
            min_dist = float('inf')

            for l_obj in lidar_objects:
                dist = np.hypot(cam_obj.x - l_obj.x, cam_obj.y - l_obj.y)
                if dist < min_dist and dist < self.association_threshold:
                    min_dist = dist
                    best_lidar = l_obj

            if best_lidar:
                # Fused object: Camera class + LiDAR high-precision position
                fused_x = 0.2 * cam_obj.x + 0.8 * best_lidar.x
                fused_y = 0.2 * cam_obj.y + 0.8 * best_lidar.y
                fused_conf = min(0.99, (cam_obj.confidence + best_lidar.confidence) / 1.8)
                
                fused = DetectedObject(
                    obj_id=cam_obj.id,
                    class_name=cam_obj.class_name, # Camera provides accurate classification
                    x=fused_x,
                    y=fused_y,
                    vx=best_lidar.vx,
                    vy=best_lidar.vy,
                    width=best_lidar.width,
                    length=best_lidar.length,
                    confidence=fused_conf
                )
                fused_objects.append(fused)
                matched_lidar_ids.add(best_lidar.id)
            else:
                # Vision-only detection
                fused_objects.append(cam_obj)

        # Add remaining LiDAR-only objects (e.g. out of camera FOV or rear)
        for l_obj in lidar_objects:
            if l_obj.id not in matched_lidar_ids:
                fused_objects.append(l_obj)

        return fused_objects
