function [detectedBoxes, lidar3DBoxes, futurePaths] = simulink_perception_block(camFrameRGB, lidarPoints, pastTracks)
% SIMULINK_PERCEPTION_BLOCK: Real-time Perception & Trajectory Pipeline
% Paste this inside a MATLAB Function Block in Simulink
%
% Inputs:
%   camFrameRGB : [640 x 640 x 3] uint8 or single camera RGB image
%   lidarPoints : [16384 x 4] single point cloud [x, y, z, intensity]
%   pastTracks  : [N x 8 x 2] single past trajectory coordinates (N obstacles)
%
% Outputs:
%   detectedBoxes : 2D Bounding Boxes & Classes from Camera YOLO
%   lidar3DBoxes  : 3D Bounding Boxes & Yaw from PointPillars LiDAR
%   futurePaths   : Predicted 12 Future Displacements (2.4s Horizon)

persistent net_cam net_lidar net_traj is_initialized

if isempty(is_initialized)
    % Initialize ONNX Networks on first step
    net_cam = importONNXNetwork('model1_camera_yolo.onnx', ...
        'InputDataPermutation', 'none', 'OutputDataPermutation', 'none');
    net_lidar = importONNXNetwork('model2_lidar.onnx', ...
        'InputDataPermutation', 'none', 'OutputDataPermutation', 'none');
    net_traj = importONNXNetwork('model3_trajectory_predictor.onnx', ...
        'InputDataPermutation', 'none', 'OutputDataPermutation', 'none');
    is_initialized = true;
end

%% 1. Camera Inference (Model 1)
imgSingle = single(camFrameRGB) / 255.0;
imgTensor = permute(imgSingle, [3 1 2]); % [3 x H x W]
imgDL = dlarray(reshape(imgTensor, [1, 3, 640, 640]), 'SSCB');
detectedBoxes = extractdata(predict(net_cam, imgDL));

%% 2. LiDAR Inference (Model 2)
lidarTensor = reshape(single(lidarPoints'), [1, 4, 16384]);
lidarDL = dlarray(lidarTensor, 'SSCB');
lidar3DBoxes = extractdata(predict(net_lidar, lidarDL));

%% 3. Trajectory Prediction (Model 3)
if ~isempty(pastTracks)
    trajDL = dlarray(single(pastTracks), 'SSCB');
    futurePaths = extractdata(predict(net_traj, trajDL));
else
    futurePaths = zeros(0, 12, 2, 'single');
end

end
