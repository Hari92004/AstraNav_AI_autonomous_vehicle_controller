from enum import Enum
import numpy as np

class DrivingBehavior(Enum):
    CRUISE = "CRUISE"
    FOLLOW_LEAD = "FOLLOW_LEAD"
    OVERTAKE = "OVERTAKE"
    YIELD = "YIELD"
    EMERGENCY_BRAKE = "EMERGENCY_BRAKE"
    POTHOLE_SWERVE = "POTHOLE_SWERVE"

class BehaviorStateMachine:
    """Stateflow-equivalent Finite State Machine for Autonomous Behavior."""
    def __init__(self, target_speed=11.11): # 40 km/h = 11.11 m/s
        self.current_state = DrivingBehavior.CRUISE
        self.target_speed = target_speed # m/s
        self.nominal_speed = target_speed

    def update(self, ego_state, risk_info, static_obstacles):
        """
        Transitions states based on TTC, proximity to slow vehicles, potholes, and cattle.
        Returns: (state, target_speed_mps, lateral_target_offset)
        """
        min_ttc = risk_info['min_ttc']
        risk_actor = risk_info['highest_risk_actor']

        # 1. Check Emergency Brake Transition
        if risk_info['is_emergency']:
            self.current_state = DrivingBehavior.EMERGENCY_BRAKE
            return self.current_state, 0.0, 0.0

        # 2. Check Pothole / Road Obstacle Ahead
        ego_x, ego_y = ego_state['x'], ego_state['y']
        for obs in static_obstacles:
            if obs['class'] == 'pothole':
                dx = obs['x'] - ego_x
                dy = obs['y'] - ego_y
                if 2.0 < dx < 25.0 and abs(dy) < 1.5:
                    self.current_state = DrivingBehavior.POTHOLE_SWERVE
                    # Swerve to opposite side of road
                    swerve_lateral = -1.8 if dy > 0 else 1.8
                    return self.current_state, self.nominal_speed * 0.7, swerve_lateral

        # 3. Check Lead Vehicle / Cattle in Path
        if risk_actor:
            rx, ry = risk_actor['current_pos']
            dx = rx - ego_x
            dy = ry - ego_y

            if 5.0 < dx < 30.0 and abs(dy) < 1.8:
                if risk_actor['class'] in ['cow_cattle', 'pedestrian']:
                    self.current_state = DrivingBehavior.YIELD
                    return self.current_state, max(2.0, self.nominal_speed * 0.4), 0.0
                elif risk_actor['class'] in ['auto_rickshaw', 'truck_bus', 'two_wheeler']:
                    # Opportunity to overtake or follow
                    lead_speed = np.hypot(risk_actor['velocity'][0], risk_actor['velocity'][1])
                    if lead_speed < (self.nominal_speed * 0.6) and dx > 15.0:
                        self.current_state = DrivingBehavior.OVERTAKE
                        return self.current_state, self.nominal_speed * 0.9, -2.5 # Overtake lane
                    else:
                        self.current_state = DrivingBehavior.FOLLOW_LEAD
                        return self.current_state, min(lead_speed, self.nominal_speed), 0.0

        # 4. Default: Cruise
        self.current_state = DrivingBehavior.CRUISE
        return self.current_state, self.nominal_speed, 0.0
