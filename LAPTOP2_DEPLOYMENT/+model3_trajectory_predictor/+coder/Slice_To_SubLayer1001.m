classdef Slice_To_SubLayer1001 < nnet.layer.Layer & nnet.layer.Formattable
    % A custom layer auto-generated while importing an ONNX network.
    %#codegen

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
        % Specify the properties of the class that will not be modified
        % after the first assignment.
        function p = matlabCodegenNontunableProperties(~)
            p = {
                % Constants, i.e., Vars, NumDims and all learnables and states
                'Vars'
                'NumDims'
                };
        end
    end


    methods(Static, Hidden)
        % Instantiate a codegenable layer instance from a MATLAB layer instance
        function this_cg = matlabCodegenToRedirected(mlInstance)
            this_cg = model3_trajectory_predictor.coder.Slice_To_SubLayer1001(mlInstance);
        end
        function this_ml = matlabCodegenFromRedirected(cgInstance)
            this_ml = model3_trajectory_predictor.Slice_To_SubLayer1001(cgInstance.Name);
            if isstruct(cgInstance.Vars)
                names = fieldnames(cgInstance.Vars);
                for i=1:numel(names)
                    fieldname = names{i};
                    this_ml.Vars.(fieldname) = dlarray(cgInstance.Vars.(fieldname));
                end
            else
                this_ml.Vars = [];
            end
            this_ml.NumDims = cgInstance.NumDims;
        end
    end

    methods
        function this = Slice_To_SubLayer1001(mlInstance)
            this.Name = mlInstance.Name;
            this.NumOutputs = 2;
            this.OutputNames = {'x_Sub_output_0', 'x_Slice_output_0'};
            if isstruct(mlInstance.Vars)
                names = fieldnames(mlInstance.Vars);
                for i=1:numel(names)
                    fieldname = names{i};
                    this.Vars.(fieldname) = model3_trajectory_predictor.coder.ops.extractIfDlarray(mlInstance.Vars.(fieldname));
                end
            else
                this.Vars = [];
            end

            this.NumDims = mlInstance.NumDims;
        end

        function [x_Sub_output_0, x_Slice_output_0] = predict(this, past_trajectory__)
            if isdlarray(past_trajectory__)
                past_trajectory_ = stripdims(past_trajectory__);
            else
                past_trajectory_ = past_trajectory__;
            end
            past_trajectoryNumDims = 3;
            past_trajectory = model3_trajectory_predictor.coder.ops.permuteInputVar(past_trajectory_, [2 3 1], 3);

            [x_Sub_output_0__, x_Slice_output_0__, x_Sub_output_0NumDims__, x_Slice_output_0NumDims__] = Slice_To_SubGraph1002(this, past_trajectory, past_trajectoryNumDims, false);
            x_Sub_output_0_ = model3_trajectory_predictor.coder.ops.permuteOutputVar(x_Sub_output_0__, [3 1 2], 3);
            x_Slice_output_0_ = model3_trajectory_predictor.coder.ops.permuteOutputVar(x_Slice_output_0__, [3 1 2], 3);

            x_Sub_output_0 = dlarray(single(x_Sub_output_0_), 'CBT');
            x_Slice_output_0 = dlarray(single(x_Slice_output_0_), 'CBT');
        end

        function [x_Sub_output_0, x_Slice_output_0, x_Sub_output_0NumDims1003, x_Slice_output_0NumDims1004] = Slice_To_SubGraph1002(this, past_trajectory, past_trajectoryNumDims, Training)

            % Execute the operators:
            % Slice:
            [indices1002, x_Slice_output_0NumDims] = model3_trajectory_predictor.coder.ops.prepareSliceArgs(past_trajectory, this.Vars.x_Constant_1_output_, this.Vars.x_Constant_2_output_, this.Vars.x_Constant_output_0, this.Vars.x_Constant_3_output_, coder.const(past_trajectoryNumDims));
            x_Slice_output_0 = past_trajectory(indices1002{:});

            % Sub:
            x_Sub_output_0 = past_trajectory - x_Slice_output_0;
            x_Sub_output_0NumDims = max(coder.const(past_trajectoryNumDims), coder.const(x_Slice_output_0NumDims));

            % Set graph output arguments
            x_Sub_output_0NumDims1003 = coder.const(x_Sub_output_0NumDims);
            x_Slice_output_0NumDims1004 = coder.const(coder.const(x_Slice_output_0NumDims));

        end

    end

end