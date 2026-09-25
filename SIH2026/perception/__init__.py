import numpy as np

class DetectedObject:
    def __init__(self, obj_id, class_name, x, y, z=0.0, vx=0.0, vy=0.0, width=1.5, length=3.0, confidence=0.9):
        self.id = obj_id
        self.class_name = class_name
        self.x = x          # Global / relative longitudinal position (meters)
        self.y = y          # Global / relative lateral position (meters)
        self.z = z          # Height (meters)
        self.vx = vx        # Longitudinal velocity (m/s)
        self.vy = vy        # Lateral velocity (m/s)
        self.width = width  # Bounding box width
        self.length = length # Bounding box length
        self.confidence = confidence

    def __repr__(self):
        return f"[{self.class_name} #{self.id} at ({self.x:.1f}, {self.y:.1f}) v=({self.vx:.1f}, {self.vy:.1f}) conf={self.confidence:.2f}]"
