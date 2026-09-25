classdef Reshape_To_AddLayer1002 < nnet.layer.Layer & nnet.layer.Formattable
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
            name = 'model3_trajectory_predictor.coder.Reshape_To_AddLayer1002';
        end
    end


    methods
        function this = Reshape_To_AddLayer1002(name)
            this.Name = name;
            this.NumInputs = 2;
            this.OutputNames = {'future_trajectory'};
        end

        function [future_trajectory] = predict(this, x_decoder_decoder_5_, x_Slice_output_0)
            if isdlarray(x_decoder_decoder_5_)
                x_decoder_decoder_5_ = stripdims(x_decoder_decoder_5_);
            end
            if isdlarray(x_Slice_output_0)
                x_Slice_output_0 = stripdims(x_Slice_output_0);
            end
            x_decoder_decoder_5_NumDims = 2;
            x_Slice_output_0NumDims = 3;
            x_decoder_decoder_5_ = model3_trajectory_predictor.ops.permuteInputVar(x_decoder_decoder_5_, [2 1], 2);
            x_Slice_output_0 = model3_trajectory_predictor.ops.permuteInputVar(x_Slice_output_0, [2 3 1], 3);

            [future_trajectory, future_trajectoryNumDims] = Reshape_To_AddGraph1005(this, x_decoder_decoder_5_, x_Slice_output_0, x_decoder_decoder_5_NumDims, x_Slice_output_0NumDims, false);
            future_trajectory = model3_trajectory_predictor.ops.permuteOutputVar(future_trajectory, ['as-is'], 3);

            future_trajectory = dlarray(single(future_trajectory), repmat('U', 1, max(2, future_trajectoryNumDims)));
        end

        function [future_trajectory] = forward(this, x_decoder_decoder_5_, x_Slice_output_0)
            if isdlarray(x_decoder_decoder_5_)
                x_decoder_decoder_5_ = stripdims(x_decoder_decoder_5_);
            end
            if isdlarray(x_Slice_output_0)
                x_Slice_output_0 = stripdims(x_Slice_output_0);
            end
            x_decoder_decoder_5_NumDims = 2;
            x_Slice_output_0NumDims = 3;
            x_decoder_decoder_5_ = model3_trajectory_predictor.ops.permuteInputVar(x_decoder_decoder_5_, [2 1], 2);
            x_Slice_output_0 = model3_trajectory_predictor.ops.permuteInputVar(x_Slice_output_0, [2 3 1], 3);

            [future_trajectory, future_trajectoryNumDims] = Reshape_To_AddGraph1005(this, x_decoder_decoder_5_, x_Slice_output_0, x_decoder_decoder_5_NumDims, x_Slice_output_0NumDims, true);
            future_trajectory = model3_trajectory_predictor.ops.permuteOutputVar(future_trajectory, ['as-is'], 3);

            future_trajectory = dlarray(single(future_trajectory), repmat('U', 1, max(2, future_trajectoryNumDims)));
        end

        function [future_trajectory, future_trajectoryNumDims1006] = Reshape_To_AddGraph1005(this, x_decoder_decoder_5_, x_Slice_output_0, x_decoder_decoder_5_NumDims, x_Slice_output_0NumDims, Training)

            % Execute the operators:
            % Reshape:
            [shape, x_Reshape_output_0NumDims] = model3_trajectory_predictor.ops.prepareReshapeArgs(x_decoder_decoder_5_, this.Vars.x_Constant_4_output_, x_decoder_decoder_5_NumDims, 0);
            x_Reshape_output_0 = reshape(x_decoder_decoder_5_, shape{:});

            % Add:
            future_trajectory = x_Slice_output_0 + x_Reshape_output_0;
            future_trajectoryNumDims = max(x_Slice_output_0NumDims, x_Reshape_output_0NumDims);

            % Set graph output arguments
            future_trajectoryNumDims1006 = future_trajectoryNumDims;

        end

    end

end