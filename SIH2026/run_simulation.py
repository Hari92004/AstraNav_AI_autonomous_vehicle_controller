import time
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle

from perception.yolo_detector import CameraDetector
from perception.lidar_processor import LidarProcessor
from perception.sensor_fusion import SensorFusionEngine
from tracking_prediction.kalman_tracker import MultiObjectTracker
from tracking_prediction.trajectory_predictor import TrajectoryPredictor
from behavior_decision.risk_assessment import RiskAssessmentEngine
from behavior_decision.behavior_state_machine import BehaviorStateMachine
from path_planning.frenet_planner import FrenetOptimalTrajectoryPlanner
from vehicle_control.bicycle_model import KinematicBicycleModel, VehicleState
from vehicle_control.controllers import PurePursuitController, PIDSpeedController
from simulation_scenarios.scenario_definitions import get_scenario_by_id
from evaluation.metrics_logger import MetricsLogger

def run_closed_loop_simulation(scenario_id=5, max_steps=80, render=True, save_plot=True):
    print(f"\n=======================================================")
    print(f"🚀 STARTING SIH 2026 CLOSED-LOOP SIMULATION: SCENARIO #{scenario_id}")
    print(f"=======================================================\n")

    # 1. Load Scenario
    scenario = get_scenario_by_id(scenario_id)
    print(f"Loaded: {scenario.name} - {scenario.description}")

    # 2. Instantiate All 7 Modules
    camera = CameraDetector()
    lidar = LidarProcessor()
    fusion = SensorFusionEngine()
    tracker = MultiObjectTracker()
    predictor = TrajectoryPredictor(horizon_sec=2.5, dt=0.2)
    risk_engine = RiskAssessmentEngine()
    fsm = BehaviorStateMachine(target_speed=9.0) # ~32 km/h
    planner = FrenetOptimalTrajectoryPlanner(max_speed=12.0)
    ego_model = KinematicBicycleModel()
    ego_state = VehicleState(x=0.0, y=0.0, yaw=0.0, v=7.0) # Start at ~25 km/h
    lat_controller = PurePursuitController(wheelbase=2.8)
    lon_controller = PIDSpeedController()
    logger = MetricsLogger(scenario.name)

    dt = 0.1
    sim_time = 0.0

    # For visualization snapshots
    snapshots = []

    for step in range(max_steps):
        t0 = time.perf_counter()

        # Step A: Update Environment / Scenario Actors
        scenario.update_actors(sim_time, dt=dt)

        # Step B: Perception (Camera + LiDAR)
        ego_pose = (ego_state.x, ego_state.y, ego_state.yaw)
        cam_dets = camera.detect_frame(scenario.actors, ego_pose)
        lidar_dets = lidar.scan_environment(scenario.actors, ego_pose)

        # Step C: Sensor Fusion
        fused_objects = fusion.fuse(cam_dets, lidar_dets)

        # Step D: Multi-Object Tracking
        tracked_actors = tracker.step(fused_objects, dt=dt)

        # Step E: Motion Prediction (1-3s horizon)
        predictions = predictor.predict(tracked_actors)

        # Step F: Behavior Decision (FSM Stateflow)
        ego_dict = {'x': ego_state.x, 'y': ego_state.y, 'vx': ego_state.v * np.cos(ego_state.yaw), 'vy': ego_state.v * np.sin(ego_state.yaw), 'yaw': ego_state.yaw}
        risk_info = risk_engine.evaluate_risk(ego_dict, predictions)
        behavior_state, target_speed, target_lateral_d = fsm.update(ego_dict, risk_info, scenario.static_obstacles)

        # Step G: Adaptive Local Path Planning (Frenet)
        # Prepare obstacles for planner: (x, y, radius)
        obstacles_for_planner = []
        for obs in scenario.static_obstacles:
            obstacles_for_planner.append((obs['x'], obs['y'], obs['radius'] + 0.5))
        for actor in tracked_actors:
            obstacles_for_planner.append((actor.x, actor.y, 1.8))
            # Also add short-term predicted positions as virtual obstacles
            if actor.track_id in predictions:
                for px, py in predictions[actor.track_id]['future_waypoints'][:3]:
                    obstacles_for_planner.append((px, py, 1.5))

        frenet_traj = planner.plan(
            s0=ego_state.x,
            c_speed=ego_state.v,
            c_d=ego_state.y,
            c_d_d=ego_state.v * np.sin(ego_state.yaw),
            c_d_dd=0.0,
            target_speed=target_speed,
            target_d=target_lateral_d,
            obstacles=obstacles_for_planner
        )

        # Step H: Vehicle Control (Pure Pursuit + PID)
        steer_cmd = lat_controller.compute_steering(ego_state, frenet_traj.x, frenet_traj.y)
        accel_cmd = lon_controller.compute_accel(ego_state.v, target_speed, dt=dt)

        # Step I: Vehicle Dynamics Update
        ego_model.step(ego_state, accel_cmd, steer_cmd, dt=dt)

        t1 = time.perf_counter()
        latency_ms = (t1 - t0) * 1000.0

        # Step J: Evaluation & Metrics Logging
        min_obs_dist = float('inf')
        for ox, oy, _ in obstacles_for_planner:
            d = np.hypot(ego_state.x - ox, ego_state.y - oy)
            if d < min_obs_dist:
                min_obs_dist = d

        logger.log_step(sim_time, ego_state, behavior_state, min_obs_dist, latency_ms)

        # Capture snapshot every 10 steps
        if step % 8 == 0 or step == max_steps - 1:
            snapshots.append({
                'time': sim_time,
                'ego_x': ego_state.x,
                'ego_y': ego_state.y,
                'ego_yaw': ego_state.yaw,
                'ego_v': ego_state.v,
                'state': behavior_state.value,
                'traj_x': list(frenet_traj.x),
                'traj_y': list(frenet_traj.y),
                'actors': [{'class': a.class_name, 'x': a.x, 'y': a.y} for a in tracked_actors],
                'static_obs': list(scenario.static_obstacles),
                'predictions': {tid: p['future_waypoints'] for tid, p in predictions.items()}
            })

        sim_time += dt

        # Stop if reached end of road
        if ego_state.x >= scenario.road_length - 5.0:
            break

    # Print Official Benchmark Report
    logger.print_report()

    # Generate Visualization Plot
    if save_plot and snapshots:
        save_simulation_results(scenario, snapshots, logger)

    return logger.compute_summary()

def save_simulation_results(scenario, snapshots, logger):
    fig, (ax_bev, ax_telemetry) = plt.subplots(2, 1, figsize=(14, 9), gridspec_kw={'height_ratios': [2, 1.2]})
    fig.patch.set_facecolor('#0F172A')

    # 1. Top Plot: Bird's Eye View (BEV) Scene
    ax_bev.set_facecolor('#1E293B')
    ax_bev.set_title(f"SIH 2026 Autonomous Navigation Simulation: {scenario.name.upper()}", color='white', fontsize=12, fontweight='bold')
    
    # Draw Road Boundaries
    road_len = scenario.road_length
    rw = scenario.road_width
    ax_bev.axhline(rw/2, color='#94A3B8', linestyle='--', linewidth=1.5, label='Road Boundary')
    ax_bev.axhline(-rw/2, color='#94A3B8', linestyle='--', linewidth=1.5)
    ax_bev.axhline(0, color='#64748B', linestyle=':', linewidth=1.0) # Virtual Centerline

    # Plot Ego Trajectory
    ax_bev.plot(logger.ego_x, logger.ego_y, color='#10B981', linewidth=2.5, label='Ego Driven Path')

    # Draw Final Frame Objects
    final_snap = snapshots[-1]
    
    # Ego vehicle box
    ego_rect = Rectangle((final_snap['ego_x'] - 1.4, final_snap['ego_y'] - 0.9), 2.8, 1.8, color='#3B82F6', zorder=5, label='Ego Vehicle')
    ax_bev.add_patch(ego_rect)

    # Static Obstacles / Potholes
    for obs in final_snap['static_obs']:
        c = Circle((obs['x'], obs['y']), obs['radius'], color='#F59E0B', alpha=0.85, label=f"Pothole / Road Obstacle" if obs == final_snap['static_obs'][0] else "")
        ax_bev.add_patch(c)
        ax_bev.text(obs['x'], obs['y'] + 1.2, f"⚠️ {obs['class']}", color='#FCD34D', fontsize=8, ha='center')

    # Dynamic Actors & Predicted Paths
    for actor in final_snap['actors']:
        color_map = {'cow_cattle': '#EC4899', 'auto_rickshaw': '#F97316', 'two_wheeler': '#A855F7', 'pedestrian': '#EF4444', 'truck_bus': '#EAB308'}
        act_color = color_map.get(actor['class'], '#60A5FA')
        ax_bev.scatter(actor['x'], actor['y'], color=act_color, s=120, zorder=6, label=f"Actor: {actor['class']}")
        ax_bev.text(actor['x'], actor['y'] + 1.2, f"{actor['class']}", color='white', fontsize=8, ha='center', fontweight='bold')

    # Draw Predictions (dotted lines)
    for tid, waypoints in final_snap['predictions'].items():
        if waypoints:
            wpx = [p[0] for p in waypoints]
            wpy = [p[1] for p in waypoints]
            ax_bev.plot(wpx, wpy, linestyle=':', color='#F43F5E', linewidth=1.5)

    # Latest Planned Frenet Path
    if final_snap['traj_x']:
        ax_bev.plot(final_snap['traj_x'], final_snap['traj_y'], color='#06B6D4', linestyle='--', linewidth=2.0, label='Planned Frenet Trajectory')

    ax_bev.set_xlim(-5, road_len + 5)
    ax_bev.set_ylim(-rw - 1.5, rw + 1.5)
    ax_bev.set_xlabel("Longitudinal Distance (meters)", color='white', fontsize=9)
    ax_bev.set_ylabel("Lateral Position (meters)", color='white', fontsize=9)
    ax_bev.tick_params(colors='white')
    ax_bev.grid(True, linestyle=':', alpha=0.3, color='#475569')
    ax_bev.legend(loc='upper right', facecolor='#0F172A', edgecolor='#334155', labelcolor='white', fontsize=8)

    # 2. Bottom Plot: Telemetry Dashboard
    ax_telemetry.set_facecolor('#1E293B')
    ax_telemetry.set_title("Vehicle Telemetry, Behavior States & Replanning Latency", color='white', fontsize=11, fontweight='bold')
    
    t_arr = logger.timestamps
    v_kmh = [v * 3.6 for v in logger.ego_v]
    
    ax_telemetry.plot(t_arr, v_kmh, color='#38BDF8', linewidth=1.8, label='Speed (km/h)')
    ax_telemetry.plot(t_arr, logger.min_clearances, color='#FBBF24', linewidth=1.5, linestyle='--', label='Min Clearance (m)')
    ax_telemetry.plot(t_arr, logger.replanning_latencies_ms, color='#A78BFA', linewidth=1.2, linestyle=':', label='Replanning Latency (ms)')

    ax_telemetry.set_xlabel("Simulation Time (seconds)", color='white', fontsize=9)
    ax_telemetry.set_ylabel("Metrics / Velocity", color='white', fontsize=9)
    ax_telemetry.tick_params(colors='white')
    ax_telemetry.grid(True, linestyle=':', alpha=0.3, color='#475569')
    ax_telemetry.legend(loc='upper right', facecolor='#0F172A', edgecolor='#334155', labelcolor='white', fontsize=8)

    plt.tight_layout()
    output_path = f"d:/SIH2026/simulation_results_scenario_{scenario.name}.png"
    plt.savefig(output_path, dpi=200)
    plt.close()
    print(f"📊 Visualization snapshot saved: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="SIH 2026 Autonomous Path Planning & Collision Avoidance Closed-Loop Simulation")
    parser.add_argument("--scenario", type=int, default=5, help="Scenario ID (1 to 5): 1=Village, 2=Intersection, 3=Highway, 4=Market, 5=Cattle Crossing")
    args = parser.parse_args()

    run_closed_loop_simulation(scenario_id=args.scenario)
