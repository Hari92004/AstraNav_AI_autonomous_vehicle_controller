% =========================================================================
% SMART INDIA HACKATHON 2026 | PROBLEM STATEMENT ID: 26037
% Organization: MathWorks | Theme: Robotics & Drones
% Title: Closed-Loop Autonomous Driving Simulation in Indian Unstructured Traffic
% =========================================================================

function main_closed_loop_sim(scenario_id)
    if nargin < 1
        scenario_id = 1; % Default: Scenario 1
    end

    fprintf('=======================================================\n');
    fprintf('🚀 SIH 2026: MATLAB CLOSED-LOOP DRIVING SIMULATION\n');
    fprintf('   Running Scenario ID: %d\n', scenario_id);
    fprintf('=======================================================\n\n');

    % 1. Create Driving Scenario
    scenario = drivingScenario('SampleTime', 0.1, 'StopTime', 15.0);

    % 2. Define Road Network (Indian Road: 7m wide, curved)
    roadCenters = [0 0 0; 30 2 0; 70 -3 0; 120 5 0; 180 0 0];
    road(scenario, roadCenters, 'Lanes', lanespec(2, 'Width', 3.5));

    % 3. Create Ego Vehicle (Autonomous Car)
    egoVehicle = vehicle(scenario, ...
        'ClassID', 1, ...
        'Length', 4.7, ...
        'Width', 1.8, ...
        'Height', 1.4, ...
        'Position', [0 0 0], ...
        'Velocity', [8 0 0]); % 8 m/s (~29 km/h)

    % 4. Add Indian Traffic Actors based on Scenario ID
    switch scenario_id
        case 1
            % Scenario 1: Unmarked Road with Pothole & Oncoming Tractor
            fprintf('Scenario 1: Unmarked Village Road with Pothole Swerve\n');
            % Pothole Obstacle
            actor(scenario, 'ClassID', 7, 'Length', 1.2, 'Width', 1.2, 'Height', 0.1, ...
                'Position', [45 -1.0 0], 'PlotColor', [0.8 0.2 0.2]);
            % Oncoming Tractor
            actor(scenario, 'ClassID', 6, 'Length', 4.5, 'Width', 2.0, 'Height', 2.2, ...
                'Position', [110 2.0 0], 'Velocity', [-5 0 0]);

        case 2
            % Scenario 2: Aggressive Auto-Rickshaw Cut-in
            fprintf('Scenario 2: Aggressive Auto-Rickshaw Lane Cut-in\n');
            autoRickshaw = actor(scenario, 'ClassID', 2, 'Length', 2.8, 'Width', 1.3, 'Height', 1.8, ...
                'Position', [15 2.5 0], 'Velocity', [9 0 0]);
            % Cut-in trajectory
            autoWaypoints = [15 2.5 0; 35 2.2 0; 55 -0.5 0; 90 -0.5 0];
            trajectory(autoRickshaw, autoWaypoints, 9);

        case 3
            % Scenario 3: Stray Cattle Crossing
            fprintf('Scenario 3: Stray Cow Suddenly Crossing Road\n');
            cow = actor(scenario, 'ClassID', 3, 'Length', 2.2, 'Width', 0.9, 'Height', 1.5, ...
                'Position', [50 -4.5 0], 'Velocity', [0 1.2 0], 'PlotColor', [0.9 0.6 0.1]);
            cowWaypoints = [50 -4.5 0; 50 -1.0 0; 50 3.0 0];
            trajectory(cow, cowWaypoints, 1.2);

        otherwise
            % Default Scenario: Stray Animal Crossing
            fprintf('Scenario: Stray Animal on Road Ahead\n');
            actor(scenario, 'ClassID', 3, 'Length', 2.0, 'Width', 0.8, 'Height', 1.4, ...
                'Position', [55 0 0], 'Velocity', [0 0 0]);
    end

    % 5. Mount Sensors on Ego Vehicle (Front Camera & Roof LiDAR)
    cameraSensor = visionDetectionGenerator( ...
        'SensorIndex', 1, ...
        'SensorLocation', [1.9 0 1.4], ...
        'MaxRange', 60, ...
        'FieldOfView', [100 20], ...
        'DetectionProbability', 0.95);

    lidarSensor = lidarPointCloudGenerator( ...
        'SensorIndex', 2, ...
        'SensorLocation', [1.0 0 1.8], ...
        'MaxRange', 80, ...
        'AzimuthLimits', [-180 180], ...
        'ElevationLimits', [-15 15]);

    % 6. Setup Visualization: Bird's Eye Plot
    fig = figure('Name', 'SIH 2026 Autonomous Driving Simulation', 'Position', [100 100 900 650]);
    bep = birdsEyePlot('Parent', gca, 'XLim', [-10 100], 'YLim', [-15 15]);
    
    % Plotters
    lanePlotter(bep);
    trackPlotter = trackPlotter(bep, 'Marker', 's', 'MarkerFaceColor', 'r');
    egoPlotter = vehiclePlotter(bep, 'MarkerFaceColor', 'b');
    visionPlotter = detectionPlotter(bep, 'Marker', 'o', 'MarkerFaceColor', 'g');

    fprintf('🎮 Running live simulation loop...\n');

    % 7. Closed-Loop Simulation Loop
    while advance(scenario)
        time = scenario.SimulationTime;
        
        % Extract ego pose & actors
        [egoPose, ~] = actorPoses(scenario);
        targetPosesList = targetPoses(egoVehicle);
        
        % Sensor readings
        [cameraDets, numVision] = cameraSensor(targetPosesList, time);
        [ptCloud, numPts] = lidarSensor(targetPosesList, time);

        % Extract positions for visualization
        if numVision > 0
            detPos = zeros(numVision, 2);
            for i = 1:numVision
                detPos(i, :) = cameraDets{i}.Measurement(1:2)';
            end
            plotDetection(visionPlotter, detPos);
        end

        % Plot Ego Vehicle
        plotVehicle(egoPlotter, [0 0], egoVehicle.Length, egoVehicle.Width, ...
            'OriginOffset', [egoVehicle.Length/2 0 0]);

        % Simple Avoidance Control Logic
        minDist = 999.0;
        for i = 1:numVision
            dist = norm(cameraDets{i}.Measurement(1:2));
            if dist < minDist
                minDist = dist;
            end
        end

        % Emergency Braking or Slow Down logic
        if minDist < 15.0
            egoVehicle.Velocity = max(egoVehicle.Velocity - [0.4 0 0], [0 0 0]);
        elseif minDist < 30.0
            egoVehicle.Velocity = max(egoVehicle.Velocity - [0.15 0 0], [3 0 0]);
        end

        pause(0.05); % Smooth animation playback
    end

    fprintf('✅ Simulation completed successfully!\n');
end
