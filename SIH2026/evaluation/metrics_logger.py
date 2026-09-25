import numpy as np

class MetricsLogger:
    """Logs and computes official SIH Benchmark Metrics."""
    def __init__(self, scenario_name):
        self.scenario_name = scenario_name
        self.timestamps = []
        self.ego_x = []
        self.ego_y = []
        self.ego_v = []
        self.ego_a = []
        self.ego_steer = []
        self.min_clearances = []
        self.replanning_latencies_ms = []
        self.state_history = []
        self.collision_occurred = False
        self.near_collisions = 0
        self.emergency_brake_events = 0

    def log_step(self, t, state, behavior_state, min_dist_to_obs, latency_ms):
        self.timestamps.append(t)
        self.ego_x.append(state.x)
        self.ego_y.append(state.y)
        self.ego_v.append(state.v)
        self.ego_a.append(state.a)
        self.ego_steer.append(state.steer)
        self.min_clearances.append(min_dist_to_obs)
        self.replanning_latencies_ms.append(latency_ms)
        self.state_history.append(behavior_state)

        if min_dist_to_obs < 0.6: # Collision threshold
            self.collision_occurred = True
        elif min_dist_to_obs < 1.5:
            self.near_collisions += 1

        if behavior_state.value == "EMERGENCY_BRAKE" and (len(self.state_history) == 1 or self.state_history[-2].value != "EMERGENCY_BRAKE"):
            self.emergency_brake_events += 1

    def compute_summary(self):
        accel_arr = np.array(self.ego_a)
        dt = 0.1
        # Jerk calculation (da/dt)
        jerk_arr = np.diff(accel_arr) / dt if len(accel_arr) > 1 else np.array([0.0])
        rms_jerk = np.sqrt(np.mean(jerk_arr ** 2)) if len(jerk_arr) > 0 else 0.0

        min_clearance = min(self.min_clearances) if self.min_clearances else 0.0
        avg_latency = np.mean(self.replanning_latencies_ms) if self.replanning_latencies_ms else 0.0
        max_latency = np.max(self.replanning_latencies_ms) if self.replanning_latencies_ms else 0.0

        summary = {
            'Scenario': self.scenario_name,
            'Completed': not self.collision_occurred,
            'Collision Count': 1 if self.collision_occurred else 0,
            'Near-Collision Count': self.near_collisions,
            'Min Obstacle Clearance (m)': round(min_clearance, 2),
            'Avg Replanning Latency (ms)': round(avg_latency, 2),
            'Max Replanning Latency (ms)': round(max_latency, 2),
            'Path Smoothness (RMS Jerk m/s^3)': round(rms_jerk, 3),
            'Emergency Braking Frequency': self.emergency_brake_events,
            'Average Speed (km/h)': round(np.mean(self.ego_v) * 3.6, 1) if self.ego_v else 0.0,
            'Max Speed (km/h)': round(np.max(self.ego_v) * 3.6, 1) if self.ego_v else 0.0
        }
        return summary

    def print_report(self):
        summary = self.compute_summary()
        print("\n" + "=" * 65)
        print(f"       SIH 2026 BENCHMARK EVALUATION: {summary['Scenario'].upper()}")
        print("=" * 65)
        for k, v in summary.items():
            status_icon = "✔️" if (k == "Completed" and v) or (k == "Collision Count" and v == 0) else ""
            print(f"  • {k:35}: {v} {status_icon}")
        print("=" * 65 + "\n")
