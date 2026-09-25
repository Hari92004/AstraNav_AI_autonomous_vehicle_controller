import numpy as np

class PurePursuitController:
    """Pure Pursuit Lateral Steering Controller."""
    def __init__(self, wheelbase=2.8, k_ld=0.2, min_ld=3.0):
        self.L = wheelbase
        self.k_ld = k_ld
        self.min_ld = min_ld

    def compute_steering(self, state, target_waypoints_x, target_waypoints_y):
        """Calculates steering angle delta to reach lookahead waypoint."""
        if not target_waypoints_x or not target_waypoints_y:
            return 0.0

        lookahead = max(self.min_ld, self.k_ld * state.v)

        # Search for waypoint at lookahead distance
        target_idx = 0
        for i, (wx, wy) in enumerate(zip(target_waypoints_x, target_waypoints_y)):
            dist = np.hypot(wx - state.x, wy - state.y)
            if dist >= lookahead:
                target_idx = i
                break
        else:
            target_idx = len(target_waypoints_x) - 1

        tx = target_waypoints_x[target_idx]
        ty = target_waypoints_y[target_idx]

        # Transform target to vehicle body coordinate frame
        dx = tx - state.x
        dy = ty - state.y
        alpha = np.arctan2(dy, dx) - state.yaw
        alpha = (alpha + np.pi) % (2 * np.pi) - np.pi

        # Pure Pursuit curvature formula: delta = arctan(2 * L * sin(alpha) / Ld)
        Ld = max(1e-3, np.hypot(dx, dy))
        steer = np.arctan2(2.0 * self.L * np.sin(alpha), Ld)
        return steer


class PIDSpeedController:
    """PID Controller for speed regulation and braking."""
    def __init__(self, kp=1.2, ki=0.1, kd=0.05):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.integral_error = 0.0
        self.prev_error = 0.0

    def compute_accel(self, current_v, target_v, dt=0.1):
        error = target_v - current_v
        self.integral_error += error * dt
        derivative = (error - self.prev_error) / max(dt, 1e-4)
        self.prev_error = error

        accel = self.kp * error + self.ki * self.integral_error + self.kd * derivative
        return accel
