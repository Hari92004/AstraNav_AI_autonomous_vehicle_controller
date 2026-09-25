classdef Reshape_To_AddLayer1002 < nnet.layer.Layer & nnet.layer.Formattable
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
            this_cg = model3_trajectory_predictor.coder.Reshape_To_AddLayer1002(mlInstance);
        end
        function this_ml = matlabCodegenFromRedirected(cgInstance)
            this_ml = model3_trajectory_predictor.Reshape_To_AddLayer1002(cgInstance.Name);
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
        function this = Reshape_To_AddLayer1002(mlInstance)
            this.Name = mlInstance.Name;
            this.NumInputs = 2;
            this.OutputNames = {'future_trajectory'};
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

        function [future_trajectory] = predict(this, x_decoder_decoder_5___, x_Slice_output_0__)
            if isdlarray(x_decoder_decoder_5___)
                x_decoder_decoder_5__ = stripdims(x_decoder_decoder_5___);
            else
                x_decoder_decoder_5__ = x_decoder_decoder_5___;
            end
            if isdlarray(x_Slice_output_0__)
                x_Slice_output_0_ = stripdims(x_Slice_output_0__);
            else
                x_Slice_output_0_ = x_Slice_output_0__;
            end
            x_decoder_decoder_5_NumDims = 2;
            x_Slice_output_0NumDims = 3;
            x_decoder_decoder_5_ = model3_trajectory_predictor.coder.ops.permuteInputVar(x_decoder_decoder_5__, [2 1], 2);
            x_Slice_output_0 = model3_trajectory_predictor.coder.ops.permuteInputVar(x_Slice_output_0_, [2 3 1], 3);

            [future_trajectory__, future_trajectoryNumDims__] = Reshape_To_AddGraph1005(this, x_decoder_decoder_5_, x_Slice_output_0, x_decoder_decoder_5_NumDims, x_Slice_output_0NumDims, false);
            future_trajectory_ = model3_trajectory_predictor.coder.ops.permuteOutputVar(future_trajectory__, ['as-is'], 3);

            future_trajectory = dlarray(single(future_trajectory_), repmat('U', 1, max(2, coder.const(future_trajectoryNumDims__))));
        end

        function [future_trajectory, future_trajectoryNumDims1006] = Reshape_To_AddGraph1005(this, x_decoder_decoder_5_, x_Slice_output_0, x_decoder_decoder_5_NumDims, x_Slice_output_0NumDims, Training)

            % Execute the operators:
            % Reshape:
            [shape1003, x_Reshape_output_0NumDims] = model3_trajectory_predictor.coder.ops.prepareReshapeArgs(x_decoder_decoder_5_, this.Vars.x_Constant_4_output_, coder.const(x_decoder_decoder_5_NumDims), 0);
            x_Reshape_output_0 = reshape(x_decoder_decoder_5_, shape1003{:});

            % Add:
            future_trajectory = x_Slice_output_0 + x_Reshape_output_0;
            future_trajectoryNumDims = max(coder.const(x_Slice_output_0NumDims), coder.const(x_Reshape_output_0NumDims));

            % Set graph output arguments
            future_trajectoryNumDims1006 = coder.const(future_trajectoryNumDims);

        end

    end

end