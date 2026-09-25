import numpy as np

class RiskAssessmentEngine:
    """Calculates Time-To-Collision (TTC) and dynamic risk scores."""
    def __init__(self, min_ttc_threshold=1.8, critical_clearance=2.0):
        self.min_ttc_threshold = min_ttc_threshold
        self.critical_clearance = critical_clearance

    def evaluate_risk(self, ego_state, predictions):
        """
        ego_state: {'x': float, 'y': float, 'vx': float, 'vy': float, 'yaw': float}
        predictions: dict from TrajectoryPredictor
        """
        min_ttc = float('inf')
        highest_risk_actor = None
        has_critical_collision_threat = False

        ego_x, ego_y = ego_state['x'], ego_state['y']
        ego_v = np.hypot(ego_state['vx'], ego_state['vy'])

        for track_id, pred in predictions.items():
            curr_x, curr_y = pred['current_pos']
            dist = np.hypot(curr_x - ego_x, curr_y - ego_y)

            # Check relative closing velocity
            rel_vx = ego_state['vx'] - pred['velocity'][0]
            
            # Simple TTC along longitudinal axis if in same corridor
            if abs(curr_y - ego_y) < 2.0 and curr_x > ego_x:
                if rel_vx > 0.1:
                    ttc = (curr_x - ego_x) / rel_vx
                    if ttc < min_ttc:
                        min_ttc = ttc
                        highest_risk_actor = pred

            # Cross-track intersection threat (e.g. cattle/pedestrian sudden crossing)
            for t_idx, (px, py) in enumerate(pred['future_waypoints']):
                t_sec = (t_idx + 1) * 0.2
                ego_pred_x = ego_x + ego_state['vx'] * t_sec
                ego_pred_y = ego_y + ego_state['vy'] * t_sec
                
                inter_dist = np.hypot(px - ego_pred_x, py - ego_pred_y)
                if inter_dist < self.critical_clearance:
                    has_critical_collision_threat = True
                    if t_sec < min_ttc:
                        min_ttc = t_sec
                        highest_risk_actor = pred

        return {
            'min_ttc': min_ttc,
            'is_emergency': min_ttc < 1.2 or (has_critical_collision_threat and min_ttc < 1.5),
            'highest_risk_actor': highest_risk_actor
        }
