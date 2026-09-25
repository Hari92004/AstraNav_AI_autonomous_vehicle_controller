classdef Slice_To_SubLayer1001 < nnet.layer.Layer & nnet.layer.Formattable
    % A custom layer auto-generated while importing an ONNX network.

    %#ok<*PROPLC>
    %#ok<*NBRAK>
    %#ok<*INUSL>
    %#ok<*VARARG>
    properties (Learnable)
    end

    properties (State)
    end

    properties
        Vars
        NumDims
    end


    methods(Static, Hidden)
        % Specify the path to the class that will be used for codegen
        function name = matlabCodegenRedirect(~)
            name = 'model3_trajectory_predictor.coder.Slice_To_SubLayer1001';
        end
    end


    methods
        function this = Slice_To_SubLayer1001(name)
            this.Name = name;
            this.NumOutputs = 2;
            this.OutputNames = {'x_Sub_output_0', 'x_Slice_output_0'};
        end

        function [x_Sub_output_0, x_Slice_output_0] = predict(this, past_trajectory)
            if isdlarray(past_trajectory)
                past_trajectory = stripdims(past_trajectory);
            end
            past_trajectoryNumDims = 3;
            past_trajectory = model3_trajectory_predictor.ops.permuteInputVar(past_trajectory, [2 3 1], 3);

            [x_Sub_output_0, x_Slice_output_0, x_Sub_output_0NumDims, x_Slice_output_0NumDims] = Slice_To_SubGraph1002(this, past_trajectory, past_trajectoryNumDims, false);
            x_Sub_output_0 = model3_trajectory_predictor.ops.permuteOutputVar(x_Sub_output_0, [3 1 2], 3);
            x_Slice_output_0 = model3_trajectory_predictor.ops.permuteOutputVar(x_Slice_output_0, [3 1 2], 3);

            x_Sub_output_0 = dlarray(single(x_Sub_output_0), 'CBT');
            x_Slice_output_0 = dlarray(single(x_Slice_output_0), 'CBT');
        end

        function [x_Sub_output_0, x_Slice_output_0] = forward(this, past_trajectory)
            if isdlarray(past_trajectory)
                past_trajectory = stripdims(past_trajectory);
            end
            past_trajectoryNumDims = 3;
            past_trajectory = model3_trajectory_predictor.ops.permuteInputVar(past_trajectory, [2 3 1], 3);

            [x_Sub_output_0, x_Slice_output_0, x_Sub_output_0NumDims, x_Slice_output_0NumDims] = Slice_To_SubGraph1002(this, past_trajectory, past_trajectoryNumDims, true);
            x_Sub_output_0 = model3_trajectory_predictor.ops.permuteOutputVar(x_Sub_output_0, [3 1 2], 3);
            x_Slice_output_0 = model3_trajectory_predictor.ops.permuteOutputVar(x_Slice_output_0, [3 1 2], 3);

            x_Sub_output_0 = dlarray(single(x_Sub_output_0), 'CBT');
            x_Slice_output_0 = dlarray(single(x_Slice_output_0), 'CBT');
        end

        function [x_Sub_output_0, x_Slice_output_0, x_Sub_output_0NumDims1003, x_Slice_output_0NumDims1004] = Slice_To_SubGraph1002(this, past_trajectory, past_trajectoryNumDims, Training)

            % Execute the operators:
            % Slice:
            [Indices, x_Slice_output_0NumDims] = model3_trajectory_predictor.ops.prepareSliceArgs(past_trajectory, this.Vars.x_Constant_1_output_, this.Vars.x_Constant_2_output_, this.Vars.x_Constant_output_0, this.Vars.x_Constant_3_output_, past_trajectoryNumDims);
            x_Slice_output_0 = past_trajectory(Indices{:});

            % Sub:
            x_Sub_output_0 = past_trajectory - x_Slice_output_0;
            x_Sub_output_0NumDims = max(past_trajectoryNumDims, x_Slice_output_0NumDims);

            % Set graph output arguments
            x_Sub_output_0NumDims1003 = x_Sub_output_0NumDims;
            x_Slice_output_0NumDims1004 = x_Slice_output_0NumDims;

        end

    end

end