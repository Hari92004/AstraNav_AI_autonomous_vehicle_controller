classdef ReduceMaxLayer1000 < nnet.layer.Layer & nnet.layer.Formattable
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
            name = 'model2_lidar.coder.ReduceMaxLayer1000';
        end
    end


    methods
        function this = ReduceMaxLayer1000(name)
            this.Name = name;
            this.OutputNames = {'x_encoder_ReduceMax_'};
        end

        function [x_encoder_ReduceMax_] = predict(this, x_encoder_Relu_2_out)
            if isdlarray(x_encoder_Relu_2_out)
                x_encoder_Relu_2_out = stripdims(x_encoder_Relu_2_out);
            end
            x_encoder_Relu_2_outNumDims = 3;
            x_encoder_Relu_2_out = model2_lidar.ops.permuteInputVar(x_encoder_Relu_2_out, [2 1 3], 3);

            [x_encoder_ReduceMax_, x_encoder_ReduceMax_NumDims] = ReduceMaxGraph1000(this, x_encoder_Relu_2_out, x_encoder_Relu_2_outNumDims, false);
            x_encoder_ReduceMax_ = model2_lidar.ops.permuteOutputVar(x_encoder_ReduceMax_, [2 1], 2);

            x_encoder_ReduceMax_ = dlarray(single(x_encoder_ReduceMax_), 'CB');
        end

        function [x_encoder_ReduceMax_] = forward(this, x_encoder_Relu_2_out)
            if isdlarray(x_encoder_Relu_2_out)
                x_encoder_Relu_2_out = stripdims(x_encoder_Relu_2_out);
            end
            x_encoder_Relu_2_outNumDims = 3;
            x_encoder_Relu_2_out = model2_lidar.ops.permuteInputVar(x_encoder_Relu_2_out, [2 1 3], 3);

            [x_encoder_ReduceMax_, x_encoder_ReduceMax_NumDims] = ReduceMaxGraph1000(this, x_encoder_Relu_2_out, x_encoder_Relu_2_outNumDims, true);
            x_encoder_ReduceMax_ = model2_lidar.ops.permuteOutputVar(x_encoder_ReduceMax_, [2 1], 2);

            x_encoder_ReduceMax_ = dlarray(single(x_encoder_ReduceMax_), 'CB');
        end

        function [x_encoder_ReduceMax_, x_encoder_ReduceMax_NumDims1002] = ReduceMaxGraph1000(this, x_encoder_Relu_2_out, x_encoder_Relu_2_outNumDims, Training)

            % Execute the operators:
            % ReduceMax:
            dims = model2_lidar.ops.prepareReduceArgs(this.Vars.ReduceMaxAxes1001, x_encoder_Relu_2_outNumDims);
            xMax = max(x_encoder_Relu_2_out, [], dims);
            [x_encoder_ReduceMax_, x_encoder_ReduceMax_NumDims] = model2_lidar.ops.onnxSqueeze(xMax, this.Vars.ReduceMaxAxes1001, x_encoder_Relu_2_outNumDims);

            % Set graph output arguments
            x_encoder_ReduceMax_NumDims1002 = x_encoder_ReduceMax_NumDims;

        end

    end

end