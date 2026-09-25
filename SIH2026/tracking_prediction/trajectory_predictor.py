import numpy as np

class TrajectoryPredictor:
    """
    Multi-Agent Trajectory Predictor for Unstructured Indian Road Traffic.
    Predicts 1.0 to 3.0 seconds into the future.
    """
    def __init__(self, horizon_sec=2.5, dt=0.2):
        self.horizon_sec = horizon_sec
        self.dt = dt
        self.num_steps = int(horizon_sec / dt)

    def predict(self, tracked_actors):
        """
        Generates predicted waypoint trajectories:
        Returns: {track_id: [(x_0, y_0), (x_1, y_1), ..., (x_N, y_N)]}
        """
        predictions = {}

        for actor in tracked_actors:
            traj = []
            curr_x = actor.x
            curr_y = actor.y
            vx = actor.vx
            vy = actor.vy

            # Non-linear motion models depending on road user class
            if actor.class_name == 'cow_cattle':
                # Cattle often have erratic stop-and-turn behavior
                # Slight lateral drift model
                drift_y = np.sign(vy) * 0.2 if abs(vy) > 0.1 else 0.0
                for t_step in range(1, self.num_steps + 1):
                    t = t_step * self.dt
                    pred_x = curr_x + vx * t
                    pred_y = curr_y + (vy + drift_y) * t
                    traj.append((pred_x, pred_y))

            elif actor.class_name == 'pedestrian':
                # Pedestrians crossing
                for t_step in range(1, self.num_steps + 1):
                    t = t_step * self.dt
                    pred_x = curr_x + vx * t
                    pred_y = curr_y + vy * t
                    traj.append((pred_x, pred_y))

            elif actor.class_name == 'two_wheeler':
                # Two-wheelers weave through traffic
                for t_step in range(1, self.num_steps + 1):
                    t = t_step * self.dt
                    pred_x = curr_x + vx * t
                    pred_y = curr_y + vy * t
                    traj.append((pred_x, pred_y))

            else:
                # Standard constant velocity model
                for t_step in range(1, self.num_steps + 1):
                    t = t_step * self.dt
                    pred_x = curr_x + vx * t
                    pred_y = curr_y + vy * t
                    traj.append((pred_x, pred_y))

            predictions[actor.track_id] = {
                'class': actor.class_name,
                'current_pos': (curr_x, curr_y),
                'velocity': (vx, vy),
                'future_waypoints': traj
            }

        return predictions
