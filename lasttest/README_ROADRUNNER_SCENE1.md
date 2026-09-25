# SIH 2026: RoadRunner Scenario Guide for Scene 1
**Image Reference:** `lasttest/scene1_urban_pothole_cow.jpg`  
**Scenario Name:** Scene 1 - Urban Bitumen Road: Pothole Avoidance & Stray Cow Swerve  
**Problem Statement:** 26037 (Autonomous Navigation in Unstructured Indian Road Traffic)

---

## 📁 Generated Files

| File Name | Format | Purpose |
| :--- | :--- | :--- |
| **`scene1_urban_pothole_cow.xodr`** | ASAM OpenDRIVE 1.6 | HD Map road network (asphalt road, lanes, shoulder, friction) for RoadRunner & CARLA |
| **`scene1_urban_pothole_cow.xosc`** | ASAM OpenSCENARIO 1.1 | Scenario definition: Ego vehicle, Stray Cow, Pothole, Auto-Rickshaw, 2-Wheeler, Pedestrian & Swerve trigger |
| **`build_and_run_scene1_roadrunner.m`** | MATLAB Script | Programmatic builder & runner for Automated Driving Toolbox & RoadRunner API |

---

## 🚦 Scene 1 Parameters (from Camera & LiDAR Model Outputs)

- **Ego Speed:** $43.2\text{ km/h}$ ($12.0\text{ m/s}$)
- **Target Maneuver:** `SWERVE AVOID` (Steering $+6.7^\circ$, Lateral offset $+1.6\text{ m}$)
- **Actors & Objects in Scenario:**
  1. 🕳️ **Pothole:** $x=31.5\text{m}, y=-1.2\text{m}, \text{dim}=1.2\times1.2\times0.1\text{m}$ (depth 11.5m ahead)
  2. 🐄 **Stray Cow (Cattle):** $x=39.5\text{m}, y=-1.8\text{m}, \text{dim}=2.2\times0.9\times1.5\text{m}$ (19.5m ahead)
  3. 🛺 **Bajaj Auto-Rickshaw:** $x=40.5\text{m}, y=+1.5\text{m}, v=4.2\text{ m/s}$ (20.5m ahead)
  4. 🏍️ **Two-Wheeler (Motorcycle):** $x=36.0\text{m}, y=-3.4\text{m}, v=5.5\text{ m/s}$
  5. 🚶 **Pedestrian:** $x=37.5\text{m}, y=-5.2\text{m}$ on shoulder

---

## 🛠️ How to Import into MathWorks RoadRunner

### Method 1: Direct OpenDRIVE / OpenSCENARIO Import in RoadRunner
1. Launch **RoadRunner** (or RoadRunner Scenario).
2. Click **File $\to$ Import $\to$ OpenDRIVE (`.xodr`)** and select `scene1_urban_pothole_cow.xodr`.
3. In RoadRunner Scenario, click **File $\to$ Import $\to$ OpenSCENARIO (`.xosc`)** and select `scene1_urban_pothole_cow.xosc`.
4. The road, asphalt textures, pothole object, stray cow, auto-rickshaws, and ego trajectory will automatically populate in 3D.
5. Click **Play / Simulate** or link to **Simulink Co-Simulation**.

---

### Method 2: Run via MATLAB Command Window
1. Open MATLAB.
2. Navigate to `d:\SIH26\lasttest` (or `d:\SIH26\LAPTOP2_DEPLOYMENT`).
3. Run:
   ```matlab
   build_and_run_scene1_roadrunner
   ```
4. This will build the scenario, show the Bird's-Eye sensor coverage plot, and execute the closed-loop swerve simulation.
