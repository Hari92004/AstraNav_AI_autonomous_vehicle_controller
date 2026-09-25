classdef FlattenLayer1000 < nnet.layer.Layer & nnet.layer.Formattable
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
            name = 'model3_trajectory_predictor.coder.FlattenLayer1000';
        end
    end


    methods
        function this = FlattenLayer1000(name)
            this.Name = name;
            this.OutputNames = {'x_Flatten_output_0'};
        end

        function [x_Flatten_output_0] = predict(this, x_Relu_1_output_0)
            if isdlarray(x_Relu_1_output_0)
                x_Relu_1_output_0 = stripdims(x_Relu_1_output_0);
            end
            x_Relu_1_output_0NumDims = 3;
            x_Relu_1_output_0 = model3_trajectory_predictor.ops.permuteInputVar(x_Relu_1_output_0, [2 1 3], 3);

            [x_Flatten_output_0, x_Flatten_output_0NumDims] = FlattenGraph1000(this, x_Relu_1_output_0, x_Relu_1_output_0NumDims, false);
            x_Flatten_output_0 = model3_trajectory_predictor.ops.permuteOutputVar(x_Flatten_output_0, [2 1], 2);

            x_Flatten_output_0 = dlarray(single(x_Flatten_output_0), 'CB');
        end

        function [x_Flatten_output_0] = forward(this, x_Relu_1_output_0)
            if isdlarray(x_Relu_1_output_0)
                x_Relu_1_output_0 = stripdims(x_Relu_1_output_0);
            end
            x_Relu_1_output_0NumDims = 3;
            x_Relu_1_output_0 = model3_trajectory_predictor.ops.permuteInputVar(x_Relu_1_output_0, [2 1 3], 3);

            [x_Flatten_output_0, x_Flatten_output_0NumDims] = FlattenGraph1000(this, x_Relu_1_output_0, x_Relu_1_output_0NumDims, true);
            x_Flatten_output_0 = model3_trajectory_predictor.ops.permuteOutputVar(x_Flatten_output_0, [2 1], 2);

            x_Flatten_output_0 = dlarray(single(x_Flatten_output_0), 'CB');
        end

        function [x_Flatten_output_0, x_Flatten_output_0NumDims1001] = FlattenGraph1000(this, x_Relu_1_output_0, x_Relu_1_output_0NumDims, Training)

            % Execute the operators:
            % Flatten:
            [dim1, dim2, x_Flatten_output_0NumDims] = model3_trajectory_predictor.ops.prepareFlattenArgs(x_Relu_1_output_0, 1, x_Relu_1_output_0NumDims);
            x_Flatten_output_0 = reshape(x_Relu_1_output_0, dim1, dim2);

            % Set graph output arguments
            x_Flatten_output_0NumDims1001 = x_Flatten_output_0NumDims;

        end

    end

end