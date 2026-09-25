import numpy as np
from . import DetectedObject

class LidarProcessor:
    """3D LiDAR Point Cloud & Range Sensor Processor."""
    def __init__(self, max_range=80.0, angular_res_deg=0.5):
        self.max_range = max_range
        self.angular_res_rad = np.radians(angular_res_deg)

    def scan_environment(self, sim_actors, ego_pose):
        """Simulates 360-degree LiDAR scan with distance, depth, and spatial geometry."""
        ego_x, ego_y, ego_yaw = ego_pose
        lidar_detections = []

        for actor in sim_actors:
            dx = actor['x'] - ego_x
            dy = actor['y'] - ego_y
            dist = np.hypot(dx, dy)

            if dist <= self.max_range:
                # LiDAR provides high precision distance measurement
                lidar_noise = np.random.normal(0, 0.05) # 5cm accuracy
                lidar_obj = DetectedObject(
                    obj_id=actor['id'],
                    class_name=actor['class'],
                    x=actor['x'] + lidar_noise,
                    y=actor['y'] + lidar_noise,
                    vx=actor.get('vx', 0.0),
                    vy=actor.get('vy', 0.0),
                    width=actor.get('width', 1.5),
                    length=actor.get('length', 3.0),
                    confidence=0.95
                )
                lidar_detections.append(lidar_obj)

        return lidar_detections
