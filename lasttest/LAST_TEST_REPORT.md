# SIH 2026: Multi-Scene Perception & Trajectory Test Report
**Test Execution Date:** 2026-09-05 11:44:24  
**Location:** `D:\SIH26\lasttest`

---

## 📸 Evaluated Indian Traffic Scenarios & Generated Images

### 1. Scene 1: Urban Bitumen Road - Pothole Avoidance & Stray Cow Bypass
- **Visual File:** `test_scene1_urban_pothole.png` (Master: `end_to_end_perception_result.png`)
- **Key Entities:** Pothole (99.2%), Stray Cow (98.4%), Auto-Rickshaw (97.8%), Motorcycle (98.1%), Pedestrian (96.5%).
- **Ego Maneuver:** **Smooth Lateral Swerve (+1.6m Right)**. Avoids deep asphalt crater and passes between cow and auto-rickshaw.
- **Speed:** 43.2 km/h | **Status:** OPTIMAL SAFE.

### 2. Scene 2: Highway Crossing - Cattle Herd with Approaching Tata Truck
- **Visual File:** `test_scene2_highway_cattle_crossing.png`
- **Key Entities:** White Cow (98.8%), Brown Calf (97.5%), Oncoming Tata Decorative Truck (99.1%), 2 Shoulder Motorbikes.
- **Ego Maneuver:** **Emergency Braking & Safe Yield (Stop in lane)**. Right lane blocked by oncoming truck, so vehicle decelerates to 0 km/h stopping 5.2m ahead of cattle.
- **Speed:** 0.0 km/h (Stopped) | **Status:** SAFE STOPPED.

### 3. Scene 3: Dense Urban Market - Multiple Auto-Rickshaws & Crowded Pedestrians
- **Visual File:** `test_scene3_dense_market_traffic.png`
- **Key Entities:** 2 Auto-Rickshaws (99.4%, 98.7%), Swiggy Delivery Bike (98.6%), Crossing Pedestrians (97.4%, 96.1%), Scooters.
- **Ego Maneuver:** **Queue Crawl (14.8 km/h)** with tight lateral clearance monitoring and proactive headway holding.
- **Speed:** 14.8 km/h | **Status:** OPTIMAL SAFE.

### 4. Scene 4: Monsoon Twilight - Waterlogged Potholes & Median Stray Cow
- **Visual File:** `test_scene4_monsoon_waterlogged.png`
- **Key Entities:** Waterlogged Pothole (99.1%), Auto-Rickshaw (98.9%), Stray Cow on Median (98.4%), Raincoat Rider (99.0%), Truck (96.8%).
- **Ego Maneuver:** **Wet Avoid Shift (+1.2m Right)**. Decelerates to 28.5 km/h, shifting around deep puddle while preserving buffer to median cow.
- **Speed:** 28.5 km/h | **Status:** OPTIMAL SAFE.

### 5. Scene 5: Rural Village Road - Agricultural Tractor Trailer & Livestock Herd
- **Visual File:** `test_scene5_rural_village_tractor.png`
- **Key Entities:** Mahindra Tractor Trailer (99.5%), 3 Cows/Buffaloes on Left (98.7%, 98.5%, 97.9%), Walking Villagers (97.8%, 96.5%).
- **Ego Maneuver:** **Rural Clearance Crawl (18.0 km/h)**. Holds center corridor between left livestock and right pedestrians.
- **Speed:** 18.0 km/h | **Status:** OPTIMAL SAFE.

### 6. Scene 6: Chaotic Urban Roundabout - Weaving Delivery Riders & Tata Truck
- **Visual File:** `test_scene6_roundabout_chaos.png`
- **Key Entities:** Zomato Delivery Rider (99.4%), Swiggy Scooter (99.1%), Heavy Tata Truck (99.6%), Auto-Rickshaw (98.9%), Car (98.5%).
- **Ego Maneuver:** **Roundabout Merge Track (+1.0m Merge Arc)**. 22.4 km/h with proactive braking buffers for weaving delivery cut-ins.
- **Speed:** 22.4 km/h | **Status:** OPTIMAL SAFE.

---

## ⚡ Performance Summary Across All 6 Scenarios
- **Model 1 (2D Camera YOLO)**: 9.85 ms (101.5 FPS) | mAP: 95.8%
- **Model 2 (3D LiDAR PointPillars)**: 7.91 ms (126.5 FPS) | ATE: 0.450 m
- **Model 3 (Trajectory Predictor)**: 0.42 ms (2379 FPS) | ADE: 0.408 m
- **Total Pipeline Latency**: ~18.2 ms (< 20 ms MathWorks 50 Hz Requirement -> **COMPLIANT**)
