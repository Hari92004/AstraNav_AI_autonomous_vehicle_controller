classdef Reshape_To_ConcatLayer1000 < nnet.layer.Layer & nnet.layer.Formattable
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
            name = 'model1_camera_yolo.coder.Reshape_To_ConcatLayer1000';
        end
    end


    methods
        function this = Reshape_To_ConcatLayer1000(name)
            this.Name = name;
            this.NumInputs = 3;
            this.OutputNames = {'detected_boxes'};
        end

        function [detected_boxes] = predict(this, x_Sigmoid_output_0, x_cls_head_Gemm_outp, x_Sigmoid_1_output_0)
            if isdlarray(x_Sigmoid_output_0)
                x_Sigmoid_output_0 = stripdims(x_Sigmoid_output_0);
            end
            if isdlarray(x_cls_head_Gemm_outp)
                x_cls_head_Gemm_outp = stripdims(x_cls_head_Gemm_outp);
            end
            if isdlarray(x_Sigmoid_1_output_0)
                x_Sigmoid_1_output_0 = stripdims(x_Sigmoid_1_output_0);
            end
            x_Sigmoid_output_0NumDims = 2;
            x_cls_head_Gemm_outpNumDims = 2;
            x_Sigmoid_1_output_0NumDims = 2;
            x_Sigmoid_output_0 = model1_camera_yolo.ops.permuteInputVar(x_Sigmoid_output_0, [2 1], 2);
            x_cls_head_Gemm_outp = model1_camera_yolo.ops.permuteInputVar(x_cls_head_Gemm_outp, [2 1], 2);
            x_Sigmoid_1_output_0 = model1_camera_yolo.ops.permuteInputVar(x_Sigmoid_1_output_0, [2 1], 2);

            [detected_boxes, detected_boxesNumDims] = Reshape_To_ConcatGraph1000(this, x_Sigmoid_output_0, x_cls_head_Gemm_outp, x_Sigmoid_1_output_0, x_Sigmoid_output_0NumDims, x_cls_head_Gemm_outpNumDims, x_Sigmoid_1_output_0NumDims, false);
            detected_boxes = model1_camera_yolo.ops.permuteOutputVar(detected_boxes, ['as-is'], 3);

            detected_boxes = dlarray(single(detected_boxes), repmat('U', 1, max(2, detected_boxesNumDims)));
        end

        function [detected_boxes] = forward(this, x_Sigmoid_output_0, x_cls_head_Gemm_outp, x_Sigmoid_1_output_0)
            if isdlarray(x_Sigmoid_output_0)
                x_Sigmoid_output_0 = stripdims(x_Sigmoid_output_0);
            end
            if isdlarray(x_cls_head_Gemm_outp)
                x_cls_head_Gemm_outp = stripdims(x_cls_head_Gemm_outp);
            end
            if isdlarray(x_Sigmoid_1_output_0)
                x_Sigmoid_1_output_0 = stripdims(x_Sigmoid_1_output_0);
            end
            x_Sigmoid_output_0NumDims = 2;
            x_cls_head_Gemm_outpNumDims = 2;
            x_Sigmoid_1_output_0NumDims = 2;
            x_Sigmoid_output_0 = model1_camera_yolo.ops.permuteInputVar(x_Sigmoid_output_0, [2 1], 2);
            x_cls_head_Gemm_outp = model1_camera_yolo.ops.permuteInputVar(x_cls_head_Gemm_outp, [2 1], 2);
            x_Sigmoid_1_output_0 = model1_camera_yolo.ops.permuteInputVar(x_Sigmoid_1_output_0, [2 1], 2);

            [detected_boxes, detected_boxesNumDims] = Reshape_To_ConcatGraph1000(this, x_Sigmoid_output_0, x_cls_head_Gemm_outp, x_Sigmoid_1_output_0, x_Sigmoid_output_0NumDims, x_cls_head_Gemm_outpNumDims, x_Sigmoid_1_output_0NumDims, true);
            detected_boxes = model1_camera_yolo.ops.permuteOutputVar(detected_boxes, ['as-is'], 3);

            detected_boxes = dlarray(single(detected_boxes), repmat('U', 1, max(2, detected_boxesNumDims)));
        end

        function [detected_boxes, detected_boxesNumDims1001] = Reshape_To_ConcatGraph1000(this, x_Sigmoid_output_0, x_cls_head_Gemm_outp, x_Sigmoid_1_output_0, x_Sigmoid_output_0NumDims, x_cls_head_Gemm_outpNumDims, x_Sigmoid_1_output_0NumDims, Training)

            % Execute the operators:
            % Reshape:
            [shape, x_Reshape_2_output_0NumDims] = model1_camera_yolo.ops.prepareReshapeArgs(x_Sigmoid_1_output_0, this.Vars.x_Constant_2_output_, x_Sigmoid_1_output_0NumDims, 0);
            x_Reshape_2_output_0 = reshape(x_Sigmoid_1_output_0, shape{:});

            % Reshape:
            [shape, x_Reshape_1_output_0NumDims] = model1_camera_yolo.ops.prepareReshapeArgs(x_cls_head_Gemm_outp, this.Vars.x_Constant_1_output_, x_cls_head_Gemm_outpNumDims, 0);
            x_Reshape_1_output_0 = reshape(x_cls_head_Gemm_outp, shape{:});

            % Reshape:
            [shape, x_Reshape_output_0NumDims] = model1_camera_yolo.ops.prepareReshapeArgs(x_Sigmoid_output_0, this.Vars.x_Constant_output_0, x_Sigmoid_output_0NumDims, 0);
            x_Reshape_output_0 = reshape(x_Sigmoid_output_0, shape{:});

            % Concat:
            [detected_boxes, detected_boxesNumDims] = model1_camera_yolo.ops.onnxConcat(-1, {x_Reshape_output_0, x_Reshape_1_output_0, x_Reshape_2_output_0}, [x_Reshape_output_0NumDims, x_Reshape_1_output_0NumDims, x_Reshape_2_output_0NumDims]);

            % Set graph output arguments
            detected_boxesNumDims1001 = detected_boxesNumDims;

        end

    end

end