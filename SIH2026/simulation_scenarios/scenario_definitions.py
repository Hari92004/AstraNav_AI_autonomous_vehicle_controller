class IndianScenario:
    """Represents an Indian road environment scenario with road boundaries, actors, and obstacles."""
    def __init__(self, name, description, road_length=120.0, road_width=7.0):
        self.name = name
        self.description = description
        self.road_length = road_length
        self.road_width = road_width
        self.actors = []
        self.static_obstacles = []

    def add_dynamic_actor(self, actor_id, class_name, x, y, vx, vy, width=1.5, length=3.0):
        self.actors.append({
            'id': actor_id,
            'class': class_name,
            'x': x,
            'y': y,
            'vx': vx,
            'vy': vy,
            'width': width,
            'length': length
        })

    def add_static_obstacle(self, obs_id, class_name, x, y, radius=1.0):
        self.static_obstacles.append({
            'id': obs_id,
            'class': class_name,
            'x': x,
            'y': y,
            'radius': radius
        })

    def update_actors(self, sim_time, dt=0.1):
        """Updates positions of dynamic actors with realistic behavior/triggers."""
        for a in self.actors:
            # Special trigger: sudden cattle crossing at t >= 2.0s
            if a['class'] == 'cow_cattle' and 'cattle_crossing' in self.name:
                if sim_time >= 1.5:
                    a['vy'] = -1.2 # Steps into ego vehicle path
            # Special trigger: pedestrian crossing
            elif a['class'] == 'pedestrian' and 'market' in self.name:
                if sim_time >= 1.0:
                    a['vy'] = 0.8

            a['x'] += a['vx'] * dt
            a['y'] += a['vy'] * dt


def get_scenario_by_id(scenario_id=5):
    """
    Returns one of the 5 mandatory SIH Indian road test scenarios:
    1: Unmarked village road
    2: Busy urban intersection without traffic signals
    3: Highway merge with slow-moving vehicles
    4: Dense market area with mixed traffic
    5: Sudden cattle-crossing event
    """
    if scenario_id == 1:
        sc = IndianScenario("unmarked_village_road", "Narrow village road with unclear boundaries, oncoming tractor, potholes")
        sc.add_dynamic_actor(101, "truck_bus", x=70.0, y=1.8, vx=-4.0, vy=0.0, width=2.2, length=5.5) # Oncoming tractor
        sc.add_dynamic_actor(102, "pedestrian", x=40.0, y=-2.8, vx=0.0, vy=0.0, width=0.6, length=0.6) # Walking on shoulder
        sc.add_static_obstacle(201, "pothole", x=30.0, y=0.0, radius=1.0)
        return sc

    elif scenario_id == 2:
        sc = IndianScenario("urban_intersection", "Unregulated 4-way urban intersection without traffic signals")
        sc.add_dynamic_actor(101, "auto_rickshaw", x=50.0, y=-5.0, vx=0.0, vy=3.5, width=1.4, length=2.6) # Cross traffic
        sc.add_dynamic_actor(102, "two_wheeler", x=65.0, y=4.0, vx=-2.0, vy=-2.0, width=0.8, length=1.8) # Weaving motorcycle
        sc.add_dynamic_actor(103, "car", x=80.0, y=0.0, vx=-3.0, vy=0.0, width=1.8, length=4.2)
        return sc

    elif scenario_id == 3:
        sc = IndianScenario("highway_merge", "Highway merge with slow-moving auto-rickshaws and trucks")
        sc.add_dynamic_actor(101, "auto_rickshaw", x=35.0, y=0.0, vx=4.5, vy=0.0, width=1.4, length=2.6) # Slow lead auto
        sc.add_dynamic_actor(102, "truck_bus", x=75.0, y=-2.0, vx=7.0, vy=0.2, width=2.4, length=7.0) # Merging truck
        return sc

    elif scenario_id == 4:
        sc = IndianScenario("dense_market", "Dense market area with pushcarts, jaywalkers, and high lateral motion")
        sc.add_dynamic_actor(101, "pedestrian", x=35.0, y=-3.0, vx=0.2, vy=0.8, width=0.6, length=0.6) # Jaywalker
        sc.add_dynamic_actor(102, "two_wheeler", x=55.0, y=1.2, vx=3.0, vy=-0.3, width=0.8, length=1.8) # Bike
        sc.add_static_obstacle(201, "pothole", x=22.0, y=-1.0, radius=0.9)
        sc.add_static_obstacle(202, "pushcart", x=48.0, y=2.2, radius=1.2) # Parked pushcart
        return sc

    else: # Default: Scenario 5 (Sudden cattle crossing)
        sc = IndianScenario("sudden_cattle_crossing", "Sudden cattle-crossing event on unstructured road")
        sc.add_dynamic_actor(101, "cow_cattle", x=42.0, y=3.2, vx=0.0, vy=0.0, width=1.2, length=2.2) # Cow steps in at t>=1.5s
        sc.add_dynamic_actor(102, "two_wheeler", x=75.0, y=-1.5, vx=-3.5, vy=0.0, width=0.8, length=1.8) # Oncoming bike
        sc.add_static_obstacle(201, "pothole", x=20.0, y=1.2, radius=0.8)
        return sc
