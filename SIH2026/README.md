# SIH 2026: Adaptive Path Planning & Collision Avoidance on Unstructured Indian Roads
**Problem Statement ID:** 26037 | **Organization:** MathWorks | **Category:** Software (Robotics & Drones)

---

## 📁 Modular Codebase Architecture

```
d:/SIH2026/
├── perception/                      # Module 1: Multi-Sensor Perception & Fusion
│   ├── __init__.py
│   ├── yolo_detector.py             # 2D Camera YOLO detector (Indian classes: auto, cow, bike, etc.)
│   ├── lidar_processor.py           # 3D LiDAR point cloud processor & range scanner
│   └── sensor_fusion.py             # Fusion of 2D Vision + 3D LiDAR depth
│
├── tracking_prediction/             # Module 2: Tracking & Multi-Agent Motion Prediction
│   ├── __init__.py
│   ├── kalman_tracker.py            # Multi-Object Tracker (persistent IDs, smoothed velocity)
│   └── trajectory_predictor.py      # Non-lane 1-3s future trajectory prediction (cattle, pedestrians)
│
├── behavior_decision/               # Module 3: Behavior Decision & Risk Engine
│   ├── __init__.py
│   ├── risk_assessment.py           # Time-To-Collision (TTC) & spatial collision risk evaluator
│   └── behavior_state_machine.py    # Stateflow FSM: CRUISE, YIELD, OVERTAKE, BRAKE, POTHOLE_SWERVE
│
├── path_planning/                   # Module 4: Adaptive Local Path Planner
│   ├── __init__.py
│   └── frenet_planner.py            # Frenet Optimal Trajectory Generation (Quintic/Quartic polynomials)
│
├── vehicle_control/                 # Module 5: Vehicle Dynamics & Controller
│   ├── __init__.py
│   ├── bicycle_model.py             # Kinematic Bicycle dynamics model (wheelbase, steering limits)
│   └── controllers.py               # Pure Pursuit lateral tracker + PID speed regulator
│
├── simulation_scenarios/            # Module 6: Indian Road Simulation Scenarios
│   ├── __init__.py
│   └── scenario_definitions.py      # 5 Mandatory SIH scenarios (Village, Market, Cattle Crossing, etc.)
│
├── evaluation/                      # Module 7: Benchmarking & Metrics Logger
│   ├── __init__.py
│   └── metrics_logger.py            # Latency (ms), Jerk (m/s³), Min Clearance, Collision checks
│
├── run_simulation.py                # Master Closed-Loop Simulation & Visualization Runner
├── generate_master_blueprint_pdf.py # Generates the clickable project PDF
├── requirements.txt                 # Dependencies
└── problemstatement.pdf             # Formatted Problem Statement PDF
```

---

## ⚡ Quick Start & Execution

### 1. Install Dependencies
```bash
conda create -n sih2026 python=3.10 -y
conda activate sih2026
pip install -r requirements.txt
```

### 2. Run Closed-Loop Simulation Scenarios

You can run any of the 5 mandatory scenarios using:

```bash
# Scenario 5: Sudden Cattle-Crossing Event (Default)
python run_simulation.py --scenario 5

# Scenario 1: Unmarked Village Road (Potholes + Oncoming Tractor)
python run_simulation.py --scenario 1

# Scenario 2: Unregulated 4-Way Urban Intersection
python run_simulation.py --scenario 2

# Scenario 3: Highway Merge with Slow Auto-rickshaws
python run_simulation.py --scenario 3

# Scenario 4: Dense Market Area with Pushcarts & Jaywalkers
python run_simulation.py --scenario 4
```

### 3. Generated Evaluation Outputs
- **Live Terminal Report:** Prints Scenario Completion, Collision Count, Minimum Clearance (m), Average & Max Replanning Latency (ms), and Comfort (RMS Jerk).
- **Visualization Plot:** Saves a Bird's Eye View (BEV) and telemetry dashboard plot `simulation_results_scenario_*.png`.

---

## 🔄 Closed-Loop Integration Flow

```
[Scenario Environment] 
      │ (Raw Actor Positions & Potholes)
      ▼
[Perception (Camera + LiDAR)] ──> [Sensor Fusion] 
                                        │
                                        ▼
                                [Kalman Tracking]
                                        │
                                        ▼
                           [Multi-Agent Trajectory Prediction]
                                        │
                                        ▼
                           [Stateflow Behavior Decision]
                                        │ (Target Speed & Offset)
                                        ▼
                           [Frenet Optimal Path Planner]
                                        │ (Smooth x, y waypoints)
                                        ▼
                           [Pure Pursuit & PID Controller]
                                        │ (Steering & Accel commands)
                                        ▼
                           [Kinematic Bicycle Model Dynamics]
                                        │
                                        ▼
                           [Metrics Logger & Live Telemetry]
```
