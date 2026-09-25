import numpy as np

class VehicleState:
    def __init__(self, x=0.0, y=0.0, yaw=0.0, v=0.0):
        self.x = x
        self.y = y
        self.yaw = yaw
        self.v = v
        self.a = 0.0
        self.steer = 0.0

class KinematicBicycleModel:
    """Standard Kinematic Bicycle Model for Autonomous Vehicle Simulation."""
    def __init__(self, wheelbase=2.8, max_steer_rad=np.radians(35), max_accel=3.5, max_brake=-6.0):
        self.L = wheelbase
        self.max_steer = max_steer_rad
        self.max_accel = max_accel
        self.max_brake = max_brake

    def step(self, state, accel_cmd, steer_cmd, dt=0.1):
        """Updates vehicle state by integrating bicycle kinematics."""
        accel = np.clip(accel_cmd, self.max_brake, self.max_accel)
        steer = np.clip(steer_cmd, -self.max_steer, self.max_steer)

        state.x += state.v * np.cos(state.yaw) * dt
        state.y += state.v * np.sin(state.yaw) * dt
        state.yaw += (state.v / self.L) * np.tan(steer) * dt
        state.yaw = (state.yaw + np.pi) % (2 * np.pi) - np.pi # Normalize angle

        state.v += accel * dt
        state.v = max(0.0, state.v) # Prevent backward slip unless in reverse
        state.a = accel
        state.steer = steer

        return state
