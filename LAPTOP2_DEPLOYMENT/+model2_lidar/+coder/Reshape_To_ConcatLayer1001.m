classdef Reshape_To_ConcatLayer1001 < nnet.layer.Layer & nnet.layer.Formattable
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
            this_cg = model2_lidar.coder.Reshape_To_ConcatLayer1001(mlInstance);
        end
        function this_ml = matlabCodegenFromRedirected(cgInstance)
            this_ml = model2_lidar.Reshape_To_ConcatLayer1001(cgInstance.Name);
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
        function this = Reshape_To_ConcatLayer1001(mlInstance)
            this.Name = mlInstance.Name;
            this.NumInputs = 3;
            this.OutputNames = {'predicted_3d_boxes'};
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

        function [predicted_3d_boxes] = predict(this, x_box_head_Gemm_outp__, x_cls_head_Gemm_outp__, x_Sigmoid_output_0__)
            if isdlarray(x_box_head_Gemm_outp__)
                x_box_head_Gemm_outp_ = stripdims(x_box_head_Gemm_outp__);
            else
                x_box_head_Gemm_outp_ = x_box_head_Gemm_outp__;
            end
            if isdlarray(x_cls_head_Gemm_outp__)
                x_cls_head_Gemm_outp_ = stripdims(x_cls_head_Gemm_outp__);
            else
                x_cls_head_Gemm_outp_ = x_cls_head_Gemm_outp__;
            end
            if isdlarray(x_Sigmoid_output_0__)
                x_Sigmoid_output_0_ = stripdims(x_Sigmoid_output_0__);
            else
                x_Sigmoid_output_0_ = x_Sigmoid_output_0__;
            end
            x_box_head_Gemm_outpNumDims = 2;
            x_cls_head_Gemm_outpNumDims = 2;
            x_Sigmoid_output_0NumDims = 2;
            x_box_head_Gemm_outp = model2_lidar.coder.ops.permuteInputVar(x_box_head_Gemm_outp_, [2 1], 2);
            x_cls_head_Gemm_outp = model2_lidar.coder.ops.permuteInputVar(x_cls_head_Gemm_outp_, [2 1], 2);
            x_Sigmoid_output_0 = model2_lidar.coder.ops.permuteInputVar(x_Sigmoid_output_0_, [2 1], 2);

            [predicted_3d_boxes__, predicted_3d_boxesNumDims__] = Reshape_To_ConcatGraph1003(this, x_box_head_Gemm_outp, x_cls_head_Gemm_outp, x_Sigmoid_output_0, x_box_head_Gemm_outpNumDims, x_cls_head_Gemm_outpNumDims, x_Sigmoid_output_0NumDims, false);
            predicted_3d_boxes_ = model2_lidar.coder.ops.permuteOutputVar(predicted_3d_boxes__, ['as-is'], 3);

            predicted_3d_boxes = dlarray(single(predicted_3d_boxes_), repmat('U', 1, max(2, coder.const(predicted_3d_boxesNumDims__))));
        end

        function [predicted_3d_boxes, predicted_3d_boxesNumDims1004] = Reshape_To_ConcatGraph1003(this, x_box_head_Gemm_outp, x_cls_head_Gemm_outp, x_Sigmoid_output_0, x_box_head_Gemm_outpNumDims, x_cls_head_Gemm_outpNumDims, x_Sigmoid_output_0NumDims, Training)

            % Execute the operators:
            % Reshape:
            [shape1002, x_Reshape_2_output_0NumDims] = model2_lidar.coder.ops.prepareReshapeArgs(x_Sigmoid_output_0, this.Vars.x_Constant_2_output_, coder.const(x_Sigmoid_output_0NumDims), 0);
            x_Reshape_2_output_0 = reshape(x_Sigmoid_output_0, shape1002{:});

            % Reshape:
            [shape1003, x_Reshape_1_output_0NumDims] = model2_lidar.coder.ops.prepareReshapeArgs(x_cls_head_Gemm_outp, this.Vars.x_Constant_1_output_, coder.const(x_cls_head_Gemm_outpNumDims), 0);
            x_Reshape_1_output_0 = reshape(x_cls_head_Gemm_outp, shape1003{:});

            % Reshape:
            [shape1004, x_Reshape_output_0NumDims] = model2_lidar.coder.ops.prepareReshapeArgs(x_box_head_Gemm_outp, this.Vars.x_Constant_output_0, coder.const(x_box_head_Gemm_outpNumDims), 0);
            x_Reshape_output_0 = reshape(x_box_head_Gemm_outp, shape1004{:});

            % Concat:
            [predicted_3d_boxes, predicted_3d_boxesNumDims] = model2_lidar.coder.ops.onnxConcat(-1, {x_Reshape_output_0, x_Reshape_1_output_0, x_Reshape_2_output_0}, [coder.const(x_Reshape_output_0NumDims), coder.const(x_Reshape_1_output_0NumDims), coder.const(x_Reshape_2_output_0NumDims)]);

            % Set graph output arguments
            predicted_3d_boxesNumDims1004 = coder.const(predicted_3d_boxesNumDims);

        end

    end

end