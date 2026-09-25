classdef FlattenLayer1000 < nnet.layer.Layer & nnet.layer.Formattable
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
            this_cg = model3_trajectory_predictor.coder.FlattenLayer1000(mlInstance);
        end
        function this_ml = matlabCodegenFromRedirected(cgInstance)
            this_ml = model3_trajectory_predictor.FlattenLayer1000(cgInstance.Name);
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
        function this = FlattenLayer1000(mlInstance)
            this.Name = mlInstance.Name;
            this.OutputNames = {'x_Flatten_output_0'};
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

        function [x_Flatten_output_0] = predict(this, x_Relu_1_output_0__)
            if isdlarray(x_Relu_1_output_0__)
                x_Relu_1_output_0_ = stripdims(x_Relu_1_output_0__);
            else
                x_Relu_1_output_0_ = x_Relu_1_output_0__;
            end
            x_Relu_1_output_0NumDims = 3;
            x_Relu_1_output_0 = model3_trajectory_predictor.coder.ops.permuteInputVar(x_Relu_1_output_0_, [2 1 3], 3);

            [x_Flatten_output_0__, x_Flatten_output_0NumDims__] = FlattenGraph1000(this, x_Relu_1_output_0, x_Relu_1_output_0NumDims, false);
            x_Flatten_output_0_ = model3_trajectory_predictor.coder.ops.permuteOutputVar(x_Flatten_output_0__, [2 1], 2);

            x_Flatten_output_0 = dlarray(single(x_Flatten_output_0_), 'CB');
        end

        function [x_Flatten_output_0, x_Flatten_output_0NumDims1001] = FlattenGraph1000(this, x_Relu_1_output_0, x_Relu_1_output_0NumDims, Training)

            % Execute the operators:
            % Flatten:
            [dim11000, dim21001, x_Flatten_output_0NumDims] = model3_trajectory_predictor.coder.ops.prepareFlattenArgs(x_Relu_1_output_0, 1, coder.const(x_Relu_1_output_0NumDims));
            x_Flatten_output_0 = reshape(x_Relu_1_output_0, dim11000, dim21001);

            % Set graph output arguments
            x_Flatten_output_0NumDims1001 = coder.const(x_Flatten_output_0NumDims);

        end

    end

end