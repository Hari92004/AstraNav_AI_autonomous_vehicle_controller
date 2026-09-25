classdef ReduceMaxLayer1000 < nnet.layer.Layer & nnet.layer.Formattable
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
            this_cg = model2_lidar.coder.ReduceMaxLayer1000(mlInstance);
        end
        function this_ml = matlabCodegenFromRedirected(cgInstance)
            this_ml = model2_lidar.ReduceMaxLayer1000(cgInstance.Name);
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
        function this = ReduceMaxLayer1000(mlInstance)
            this.Name = mlInstance.Name;
            this.OutputNames = {'x_encoder_ReduceMax_'};
            if isstruct(mlInstance.Vars)
                names = fieldnames(mlInstance.Vars);
                for i=1:numel(names)
                    fieldname = names{i};
                    this.Vars.(fieldname) = model2_lidar.coder.ops.extractIfDlarray(mlInstance.Vars.(fieldname));
                end
            else
                this.Vars = [];
            end

            this.NumDims = mlInstance.NumDims;
        end

        function [x_encoder_ReduceMax_] = predict(this, x_encoder_Relu_2_out__)
            if isdlarray(x_encoder_Relu_2_out__)
                x_encoder_Relu_2_out_ = stripdims(x_encoder_Relu_2_out__);
            else
                x_encoder_Relu_2_out_ = x_encoder_Relu_2_out__;
            end
            x_encoder_Relu_2_outNumDims = 3;
            x_encoder_Relu_2_out = model2_lidar.coder.ops.permuteInputVar(x_encoder_Relu_2_out_, [2 1 3], 3);

            [x_encoder_ReduceMax___, x_encoder_ReduceMax_NumDims__] = ReduceMaxGraph1000(this, x_encoder_Relu_2_out, x_encoder_Relu_2_outNumDims, false);
            x_encoder_ReduceMax__ = model2_lidar.coder.ops.permuteOutputVar(x_encoder_ReduceMax___, [2 1], 2);

            x_encoder_ReduceMax_ = dlarray(single(x_encoder_ReduceMax__), 'CB');
        end

        function [x_encoder_ReduceMax_, x_encoder_ReduceMax_NumDims1002] = ReduceMaxGraph1000(this, x_encoder_Relu_2_out, x_encoder_Relu_2_outNumDims, Training)

            % Execute the operators:
            % ReduceMax:
            dims1000 = model2_lidar.coder.ops.prepareReduceArgs(this.Vars.ReduceMaxAxes1001, coder.const(x_encoder_Relu_2_outNumDims));
            xReduced1001 = max(x_encoder_Relu_2_out, [], dims1000);
            [x_encoder_ReduceMax_, x_encoder_ReduceMax_NumDims] = model2_lidar.coder.ops.onnxSqueeze(xReduced1001, this.Vars.ReduceMaxAxes1001, coder.const(x_encoder_Relu_2_outNumDims));

            % Set graph output arguments
            x_encoder_ReduceMax_NumDims1002 = coder.const(x_encoder_ReduceMax_NumDims);

        end

    end

end