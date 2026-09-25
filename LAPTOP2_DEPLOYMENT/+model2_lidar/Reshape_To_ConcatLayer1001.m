classdef Reshape_To_ConcatLayer1001 < nnet.layer.Layer & nnet.layer.Formattable
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
            name = 'model2_lidar.coder.Reshape_To_ConcatLayer1001';
        end
    end


    methods
        function this = Reshape_To_ConcatLayer1001(name)
            this.Name = name;
            this.NumInputs = 3;
            this.OutputNames = {'predicted_3d_boxes'};
        end

        function [predicted_3d_boxes] = predict(this, x_box_head_Gemm_outp, x_cls_head_Gemm_outp, x_Sigmoid_output_0)
            if isdlarray(x_box_head_Gemm_outp)
                x_box_head_Gemm_outp = stripdims(x_box_head_Gemm_outp);
            end
            if isdlarray(x_cls_head_Gemm_outp)
                x_cls_head_Gemm_outp = stripdims(x_cls_head_Gemm_outp);
            end
            if isdlarray(x_Sigmoid_output_0)
                x_Sigmoid_output_0 = stripdims(x_Sigmoid_output_0);
            end
            x_box_head_Gemm_outpNumDims = 2;
            x_cls_head_Gemm_outpNumDims = 2;
            x_Sigmoid_output_0NumDims = 2;
            x_box_head_Gemm_outp = model2_lidar.ops.permuteInputVar(x_box_head_Gemm_outp, [2 1], 2);
            x_cls_head_Gemm_outp = model2_lidar.ops.permuteInputVar(x_cls_head_Gemm_outp, [2 1], 2);
            x_Sigmoid_output_0 = model2_lidar.ops.permuteInputVar(x_Sigmoid_output_0, [2 1], 2);

            [predicted_3d_boxes, predicted_3d_boxesNumDims] = Reshape_To_ConcatGraph1003(this, x_box_head_Gemm_outp, x_cls_head_Gemm_outp, x_Sigmoid_output_0, x_box_head_Gemm_outpNumDims, x_cls_head_Gemm_outpNumDims, x_Sigmoid_output_0NumDims, false);
            predicted_3d_boxes = model2_lidar.ops.permuteOutputVar(predicted_3d_boxes, ['as-is'], 3);

            predicted_3d_boxes = dlarray(single(predicted_3d_boxes), repmat('U', 1, max(2, predicted_3d_boxesNumDims)));
        end

        function [predicted_3d_boxes] = forward(this, x_box_head_Gemm_outp, x_cls_head_Gemm_outp, x_Sigmoid_output_0)
            if isdlarray(x_box_head_Gemm_outp)
                x_box_head_Gemm_outp = stripdims(x_box_head_Gemm_outp);
            end
            if isdlarray(x_cls_head_Gemm_outp)
                x_cls_head_Gemm_outp = stripdims(x_cls_head_Gemm_outp);
            end
            if isdlarray(x_Sigmoid_output_0)
                x_Sigmoid_output_0 = stripdims(x_Sigmoid_output_0);
            end
            x_box_head_Gemm_outpNumDims = 2;
            x_cls_head_Gemm_outpNumDims = 2;
            x_Sigmoid_output_0NumDims = 2;
            x_box_head_Gemm_outp = model2_lidar.ops.permuteInputVar(x_box_head_Gemm_outp, [2 1], 2);
            x_cls_head_Gemm_outp = model2_lidar.ops.permuteInputVar(x_cls_head_Gemm_outp, [2 1], 2);
            x_Sigmoid_output_0 = model2_lidar.ops.permuteInputVar(x_Sigmoid_output_0, [2 1], 2);

            [predicted_3d_boxes, predicted_3d_boxesNumDims] = Reshape_To_ConcatGraph1003(this, x_box_head_Gemm_outp, x_cls_head_Gemm_outp, x_Sigmoid_output_0, x_box_head_Gemm_outpNumDims, x_cls_head_Gemm_outpNumDims, x_Sigmoid_output_0NumDims, true);
            predicted_3d_boxes = model2_lidar.ops.permuteOutputVar(predicted_3d_boxes, ['as-is'], 3);

            predicted_3d_boxes = dlarray(single(predicted_3d_boxes), repmat('U', 1, max(2, predicted_3d_boxesNumDims)));
        end

        function [predicted_3d_boxes, predicted_3d_boxesNumDims1004] = Reshape_To_ConcatGraph1003(this, x_box_head_Gemm_outp, x_cls_head_Gemm_outp, x_Sigmoid_output_0, x_box_head_Gemm_outpNumDims, x_cls_head_Gemm_outpNumDims, x_Sigmoid_output_0NumDims, Training)

            % Execute the operators:
            % Reshape:
            [shape, x_Reshape_2_output_0NumDims] = model2_lidar.ops.prepareReshapeArgs(x_Sigmoid_output_0, this.Vars.x_Constant_2_output_, x_Sigmoid_output_0NumDims, 0);
            x_Reshape_2_output_0 = reshape(x_Sigmoid_output_0, shape{:});

            % Reshape:
            [shape, x_Reshape_1_output_0NumDims] = model2_lidar.ops.prepareReshapeArgs(x_cls_head_Gemm_outp, this.Vars.x_Constant_1_output_, x_cls_head_Gemm_outpNumDims, 0);
            x_Reshape_1_output_0 = reshape(x_cls_head_Gemm_outp, shape{:});

            % Reshape:
            [shape, x_Reshape_output_0NumDims] = model2_lidar.ops.prepareReshapeArgs(x_box_head_Gemm_outp, this.Vars.x_Constant_output_0, x_box_head_Gemm_outpNumDims, 0);
            x_Reshape_output_0 = reshape(x_box_head_Gemm_outp, shape{:});

            % Concat:
            [predicted_3d_boxes, predicted_3d_boxesNumDims] = model2_lidar.ops.onnxConcat(-1, {x_Reshape_output_0, x_Reshape_1_output_0, x_Reshape_2_output_0}, [x_Reshape_output_0NumDims, x_Reshape_1_output_0NumDims, x_Reshape_2_output_0NumDims]);

            % Set graph output arguments
            predicted_3d_boxesNumDims1004 = predicted_3d_boxesNumDims;

        end

    end

end