classdef Reshape_To_ConcatLayer1000 < nnet.layer.Layer & nnet.layer.Formattable
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
            this_cg = model1_camera_yolo.coder.Reshape_To_ConcatLayer1000(mlInstance);
        end
        function this_ml = matlabCodegenFromRedirected(cgInstance)
            this_ml = model1_camera_yolo.Reshape_To_ConcatLayer1000(cgInstance.Name);
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
        function this = Reshape_To_ConcatLayer1000(mlInstance)
            this.Name = mlInstance.Name;
            this.NumInputs = 3;
            this.OutputNames = {'detected_boxes'};
            if isstruct(mlInstance.Vars)
                names = fieldnames(mlInstance.Vars);
                for i=1:numel(names)
                    fieldname = names{i};
                    this.Vars.(fieldname) = model1_camera_yolo.coder.ops.extractIfDlarray(mlInstance.Vars.(fieldname));
                end
            else
                this.Vars = [];
            end

            this.NumDims = mlInstance.NumDims;
        end

        function [detected_boxes] = predict(this, x_Sigmoid_output_0__, x_cls_head_Gemm_outp__, x_Sigmoid_1_output_0__)
            if isdlarray(x_Sigmoid_output_0__)
                x_Sigmoid_output_0_ = stripdims(x_Sigmoid_output_0__);
            else
                x_Sigmoid_output_0_ = x_Sigmoid_output_0__;
            end
            if isdlarray(x_cls_head_Gemm_outp__)
                x_cls_head_Gemm_outp_ = stripdims(x_cls_head_Gemm_outp__);
            else
                x_cls_head_Gemm_outp_ = x_cls_head_Gemm_outp__;
            end
            if isdlarray(x_Sigmoid_1_output_0__)
                x_Sigmoid_1_output_0_ = stripdims(x_Sigmoid_1_output_0__);
            else
                x_Sigmoid_1_output_0_ = x_Sigmoid_1_output_0__;
            end
            x_Sigmoid_output_0NumDims = 2;
            x_cls_head_Gemm_outpNumDims = 2;
            x_Sigmoid_1_output_0NumDims = 2;
            x_Sigmoid_output_0 = model1_camera_yolo.coder.ops.permuteInputVar(x_Sigmoid_output_0_, [2 1], 2);
            x_cls_head_Gemm_outp = model1_camera_yolo.coder.ops.permuteInputVar(x_cls_head_Gemm_outp_, [2 1], 2);
            x_Sigmoid_1_output_0 = model1_camera_yolo.coder.ops.permuteInputVar(x_Sigmoid_1_output_0_, [2 1], 2);

            [detected_boxes__, detected_boxesNumDims__] = Reshape_To_ConcatGraph1000(this, x_Sigmoid_output_0, x_cls_head_Gemm_outp, x_Sigmoid_1_output_0, x_Sigmoid_output_0NumDims, x_cls_head_Gemm_outpNumDims, x_Sigmoid_1_output_0NumDims, false);
            detected_boxes_ = model1_camera_yolo.coder.ops.permuteOutputVar(detected_boxes__, ['as-is'], 3);

            detected_boxes = dlarray(single(detected_boxes_), repmat('U', 1, max(2, coder.const(detected_boxesNumDims__))));
        end

        function [detected_boxes, detected_boxesNumDims1001] = Reshape_To_ConcatGraph1000(this, x_Sigmoid_output_0, x_cls_head_Gemm_outp, x_Sigmoid_1_output_0, x_Sigmoid_output_0NumDims, x_cls_head_Gemm_outpNumDims, x_Sigmoid_1_output_0NumDims, Training)

            % Execute the operators:
            % Reshape:
            [shape1000, x_Reshape_2_output_0NumDims] = model1_camera_yolo.coder.ops.prepareReshapeArgs(x_Sigmoid_1_output_0, this.Vars.x_Constant_2_output_, coder.const(x_Sigmoid_1_output_0NumDims), 0);
            x_Reshape_2_output_0 = reshape(x_Sigmoid_1_output_0, shape1000{:});

            % Reshape:
            [shape1001, x_Reshape_1_output_0NumDims] = model1_camera_yolo.coder.ops.prepareReshapeArgs(x_cls_head_Gemm_outp, this.Vars.x_Constant_1_output_, coder.const(x_cls_head_Gemm_outpNumDims), 0);
            x_Reshape_1_output_0 = reshape(x_cls_head_Gemm_outp, shape1001{:});

            % Reshape:
            [shape1002, x_Reshape_output_0NumDims] = model1_camera_yolo.coder.ops.prepareReshapeArgs(x_Sigmoid_output_0, this.Vars.x_Constant_output_0, coder.const(x_Sigmoid_output_0NumDims), 0);
            x_Reshape_output_0 = reshape(x_Sigmoid_output_0, shape1002{:});

            % Concat:
            [detected_boxes, detected_boxesNumDims] = model1_camera_yolo.coder.ops.onnxConcat(-1, {x_Reshape_output_0, x_Reshape_1_output_0, x_Reshape_2_output_0}, [coder.const(x_Reshape_output_0NumDims), coder.const(x_Reshape_1_output_0NumDims), coder.const(x_Reshape_2_output_0NumDims)]);

            % Set graph output arguments
            detected_boxesNumDims1001 = coder.const(detected_boxesNumDims);

        end

    end

end