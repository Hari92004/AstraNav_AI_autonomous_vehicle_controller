import sys
import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and draw total page numbers and header/footer."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        
        # Header (pages after page 1)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#334155"))
            self.drawString(54, 11 * inch - 36, "SIH 2026 | PS ID 26037: AI MODEL TRAINING & DATASET MANUAL")
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "MATHWORKS / AUTONOMOUS SYSTEMS")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
        
        # Footer (all pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 44, 8.5 * inch - 54, 44)
        
        self.drawString(54, 30, "AI Training & Model Deployment Guide • Smart India Hackathon 2026")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 30, page_str)
        
        self.restoreState()

def build_training_pdf(output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=45,
        rightMargin=45,
        topMargin=45,
        bottomMargin=45
    )

    styles = getSampleStyleSheet()

    # Color Palette
    c_primary = colors.HexColor("#0F3D64")      # Deep Professional Navy
    c_secondary = colors.HexColor("#0284C7")    # Sky Blue Accent
    c_dark = colors.HexColor("#0F172A")         # Slate Dark
    c_body = colors.HexColor("#334155")         # Charcoal Body
    c_card_bg = colors.HexColor("#F8FAFC")      # Soft Light Card
    c_border = colors.HexColor("#E2E8F0")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=14.5, leading=18,
        textColor=c_primary, spaceAfter=3
    )

    h1_style = ParagraphStyle(
        'SectionH1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=11, leading=14,
        textColor=c_primary, spaceBefore=10, spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=9, leading=12,
        textColor=colors.HexColor("#0369A1"), spaceBefore=6, spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.2, leading=11.5,
        textColor=c_body, spaceAfter=3
    )

    bullet_style = ParagraphStyle(
        'BulletText', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.2, leading=11.5,
        textColor=c_body, leftIndent=10, spaceAfter=2
    )

    code_block_style = ParagraphStyle(
        'CodeBlock', parent=styles['Normal'],
        fontName='Courier', fontSize=7.2, leading=9.8,
        textColor=colors.HexColor("#0F172A")
    )

    table_header = ParagraphStyle(
        'TableHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=7.8, leading=10,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TableCell', parent=styles['Normal'],
        fontName='Helvetica', fontSize=7.5, leading=9.8,
        textColor=c_dark
    )

    badge_style = ParagraphStyle(
        'BadgeText', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=10,
        textColor=colors.white
    )

    story = []

    # =========================================================================
    # 1. HEADER BANNER
    # =========================================================================
    top_bar_data = [
        [
            Paragraph("<b>SMART INDIA HACKATHON 2026 | PROBLEM ID: 26037</b>", badge_style),
            Paragraph("<b>Theme:</b> Robotics & Drones &nbsp;|&nbsp; <b>Organization:</b> MathWorks", ParagraphStyle('RightBadge', parent=badge_style, alignment=2))
        ]
    ]
    top_bar = Table(top_bar_data, colWidths=[260, 262])
    top_bar.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_primary),
        ('PADDING', (0, 0), (-1, -1), 4),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(top_bar)

    title_box_data = [
        [
            Paragraph("<b>AI Models Suite Training, Datasets Repository & MATLAB Deployment Manual</b>", title_style)
        ],
        [
            Paragraph("<i>A Definitive Blueprint covering the 3 Core AI Models (2D YOLOv8 Vision, 3D LiDAR PointPillars, and Seq2Seq GRU Trajectory Predictor), Full Datasets Links, Sizes, GPU Training Commands, and MATLAB ONNX Integration.</i>", body_style)
        ]
    ]
    title_box = Table(title_box_data, colWidths=[522])
    title_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LINEBELOW', (0, -1), (-1, -1), 1.5, c_secondary),
    ]))
    story.append(title_box)
    story.append(Spacer(1, 4))

    # =========================================================================
    # 2. REQUIRED 3 AI MODELS ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("1. The 3 Core AI Models Architecture & Detailed Roles", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=1, spaceAfter=4))

    models_overview_data = [
        [
            Paragraph("Model Name & Architecture", table_header),
            Paragraph("Sensor Input", table_header),
            Paragraph("Specific Detection / Prediction Objective", table_header),
            Paragraph("Deployment Format", table_header)
        ],
        [
            Paragraph("<b>Model 1: 2D Vision Perception</b><br/>YOLOv8m / YOLO11m<br/>(PyTorch Ultralytics)", table_cell),
            Paragraph("Front Windshield RGB Camera (60m Range)", table_cell),
            Paragraph("Detects and classifies <b>7 Indian Traffic Classes:</b><br/>• Auto-rickshaws &bull; Stray Cattle/Cows<br/>• Pedestrians &bull; Two-wheelers / Bikes<br/>• Potholes & Cracks &bull; Trucks/Buses &bull; Cars", table_cell),
            Paragraph("PyTorch (<code>.pt</code>)<br/>ONNX (<code>best.onnx</code>)", table_cell)
        ],
        [
            Paragraph("<b>Model 2: 3D LiDAR Perception</b><br/>PointPillars / CenterPoint<br/>(Point Cloud NN)", table_cell),
            Paragraph("Roof 360° LiDAR (80m, 32-beam)", table_cell),
            Paragraph("Processes 3D point cloud clusters (X,Y,Z,Intensity) to estimate <b>3D Bounding Boxes</b> (X, Y, Z, length, width, height) and precise obstacle distances.", table_cell),
            Paragraph("3D BBoxes<br/>Point Clusters", table_cell)
        ],
        [
            Paragraph("<b>Model 3: Motion Prediction</b><br/>Seq2Seq GRU / Social-LSTM<br/>(Recurrent Neural Net)", table_cell),
            Paragraph("Past 1.5–2.0s Tracker Positions", table_cell),
            Paragraph("Forecasts future non-lane trajectory paths over <b>1.0 to 3.0s horizon</b> for erratic cattle crossing, pedestrians, and weaving bikes.", table_cell),
            Paragraph("PyTorch (<code>.pth</code>)<br/>ONNX (<code>trajectory.onnx</code>)", table_cell)
        ]
    ]

    models_table = Table(models_overview_data, colWidths=[125, 95, 215, 87])
    models_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_card_bg]),
        ('PADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(models_table)
    story.append(Spacer(1, 5))

    # =========================================================================
    # 3. COMPREHENSIVE DATASETS REPOSITORY TABLE
    # =========================================================================
    story.append(Paragraph("2. Official Datasets Repository, Direct Links & Download Sizes", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=1, spaceAfter=4))

    datasets_table_data = [
        [
            Paragraph("Dataset Name", table_header),
            Paragraph("Target AI Model", table_header),
            Paragraph("Direct Download / Source Link", table_header),
            Paragraph("Size", table_header),
            Paragraph("Dataset Content & Format", table_header)
        ],
        [
            Paragraph("<b>Roboflow Indian Traffic & Cattle Suite</b><br/>⭐ <i>(Recommended / Fast)</i>", table_cell),
            Paragraph("Model 1 (YOLOv8 Vision)", table_cell),
            Paragraph("<font color='#0284C7'><u>universe.roboflow.com/search?q=indian+traffic</u></font><br/><font color='#0284C7'><u>universe.roboflow.com/search?q=indian+cattle</u></font>", table_cell),
            Paragraph("<b>~350 MB</b>", table_cell),
            Paragraph("5,000+ pre-annotated Indian road images in YOLO format (.txt bboxes) for Auto, Cow, Bike, Pothole.", table_cell)
        ],
        [
            Paragraph("<b>Indian Driving Dataset (IDD)</b><br/><i>(IIIT Hyderabad Benchmark)</i>", table_cell),
            Paragraph("Model 1 (YOLOv8 Vision)", table_cell),
            Paragraph("<font color='#0284C7'><u>idd.insaan.iiit.ac.in</u></font>", table_cell),
            Paragraph("<b>~12 GB</b>", table_cell),
            Paragraph("40,000+ high-density Indian traffic frames from Bangalore/Hyderabad with unstructured roads and dense obstacles.", table_cell)
        ],
        [
            Paragraph("<b>Roboflow Pothole & Road Anomaly Dataset</b>", table_cell),
            Paragraph("Model 1 (YOLOv8 Vision)", table_cell),
            Paragraph("<font color='#0284C7'><u>universe.roboflow.com/search?q=pothole</u></font>", table_cell),
            Paragraph("<b>~180 MB</b>", table_cell),
            Paragraph("2,500+ annotated images of asphalt road cracks, deep potholes, and surface irregularities.", table_cell)
        ],
        [
            Paragraph("<b>nuScenes Mini Suite (LiDAR + Camera)</b><br/>⭐ <i>(Recommended LiDAR)</i>", table_cell),
            Paragraph("Model 2 (3D LiDAR)", table_cell),
            Paragraph("<font color='#0284C7'><u>nuscenes.org/download</u></font><br/>(<code>v1.0-mini.tgz</code>)", table_cell),
            Paragraph("<b>~3.8 GB</b>", table_cell),
            Paragraph("Calibrated 360° LiDAR 32-beam point clouds (.pcd) with 3D ground truth bounding boxes.", table_cell)
        ],
        [
            Paragraph("<b>KITTI 3D Vision Benchmark</b>", table_cell),
            Paragraph("Model 2 (3D LiDAR)", table_cell),
            Paragraph("<font color='#0284C7'><u>cvlibs.net/datasets/kitti/eval_object.php?obj_benchmark=3d</u></font>", table_cell),
            Paragraph("<b>~12 GB</b>", table_cell),
            Paragraph("Velodyne 64-beam 3D spatial point clouds and stereo camera calibrated benchmark.", table_cell)
        ],
        [
            Paragraph("<b>Built-in Indian Trajectory Generator</b><br/>⭐ <i>(Fastest / Zero Download)</i>", table_cell),
            Paragraph("Model 3 (Trajectory Predictor)", table_cell),
            Paragraph("Included in Repo Script:<br/><code>training_suite/train_trajectory_predictor.py</code>", table_cell),
            Paragraph("<b>0 MB<br/>(Instant)</b>", table_cell),
            Paragraph("Generates 5,000+ non-lane trajectory paths (weaving two-wheelers, cattle crossing, pedestrian darting).", table_cell)
        ],
        [
            Paragraph("<b>INTERACTION Dataset</b>", table_cell),
            Paragraph("Model 3 (Trajectory Predictor)", table_cell),
            Paragraph("<font color='#0284C7'><u>interaction-dataset.com</u></font>", table_cell),
            Paragraph("<b>~2.5 GB</b>", table_cell),
            Paragraph("Unstructured roundabout, merging and multi-agent interaction motion tracks.", table_cell)
        ]
    ]

    datasets_table = Table(datasets_table_data, colWidths=[115, 75, 140, 50, 142])
    datasets_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_card_bg]),
        ('PADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(datasets_table)
    story.append(Spacer(1, 5))

    # =========================================================================
    # 4. STEP-BY-STEP TRAINING PIPELINE (YOLOv8, LIDAR & TRAJECTORY)
    # =========================================================================
    story.append(Paragraph("3. Step-by-Step AI Models Training Execution", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=1, spaceAfter=4))

    story.append(Paragraph("<b>A. Training Model 1: 2D Vision Object Detector (YOLOv8 / YOLO11)</b>", h2_style))
    yolo_cmd_box = Table([[
        Paragraph(
            "<font color='#0284C7'># 1. Navigate to training suite and execute YOLO training</font><br/>"
            "cd d:\\SIH2026\\training_suite<br/>"
            "python train_yolo_detector.py<br/><br/>"
            "<b>Configured Hyperparameters:</b><br/>"
            "• Base Weights: <code>yolov8m.pt</code> (Transfer Learning with pre-trained COCO weights)<br/>"
            "• Epochs: 50 | Batch Size: 16 (or 8 for 4GB RTX 2050) | Image Resolution: 640x640<br/>"
            "• Augmentations: Mosaic=1.0, Flipud=0.5, HSV Color Jitter for sunny/rainy Indian roads<br/>"
            "• Export Output: Generates <code>best.pt</code> and MATLAB-compatible <code>best.onnx</code>",
            code_block_style
        )
    ]], colWidths=[522])
    yolo_cmd_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(yolo_cmd_box)
    story.append(Spacer(1, 3))

    story.append(Paragraph("<b>B. Training Model 2 & 3: 3D LiDAR & Trajectory Predictor Neural Nets</b>", h2_style))
    other_models_box = Table([[
        Paragraph(
            "<font color='#0284C7'># 2. Train Multi-Agent Seq2Seq GRU Trajectory Predictor</font><br/>"
            "python train_trajectory_predictor.py<br/>"
            "<i>Saves: <code>trajectory_model.pth</code> and <code>trajectory_predictor.onnx</code> (Loss: ADE &lt; 0.35m)</i><br/><br/>"
            "<font color='#0284C7'># 3. Train 3D LiDAR Point Cloud Cluster Detector</font><br/>"
            "cd d:\\SIH2026\\demo_training_suite<br/>"
            "python 02_train_lidar_detector.py &nbsp;&nbsp;&nbsp;&nbsp;<font color='#0284C7'># Extracts 3D Bounding Box spatial depths</font>",
            code_block_style
        )
    ]], colWidths=[522])
    other_models_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(other_models_box)
    story.append(Spacer(1, 5))

    # =========================================================================
    # 5. METRICS BENCHMARKS & VERIFICATION
    # =========================================================================
    story.append(Paragraph("4. Post-Training Validation Benchmarks & Verification", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=1, spaceAfter=4))

    metrics_table_data = [
        [
            Paragraph("Evaluation Metric", table_header),
            Paragraph("Target Benchmark", table_header),
            Paragraph("Quality Assessment & SIH Evaluation Criterion", table_header)
        ],
        [
            Paragraph("<b>mAP@0.50 (Mean Average Precision)</b>", table_cell),
            Paragraph("<b>&gt; 0.85 (85%+)</b>", table_cell),
            Paragraph("<b>🌟 Production Ready:</b> Reliable detection of Auto-rickshaws, cattle, pedestrians and potholes under harsh Indian lighting.", table_cell)
        ],
        [
            Paragraph("<b>mAP@0.50:0.95 (Strict IoU)</b>", table_cell),
            Paragraph("<b>&gt; 0.55 (55%+)</b>", table_cell),
            Paragraph("Tight spatial bounding-box localization around obstacle borders.", table_cell)
        ],
        [
            Paragraph("<b>Precision & Recall</b>", table_cell),
            Paragraph("<b>&gt; 0.80 (80%+)</b>", table_cell),
            Paragraph("Zero false alarms (avoids phantom emergency braking) and zero missed obstacles.", table_cell)
        ],
        [
            Paragraph("<b>Trajectory Prediction ADE</b>", table_cell),
            Paragraph("<b>&lt; 0.35 meters</b>", table_cell),
            Paragraph("Average Displacement Error well within 1.5m clearance margin, enabling safe Frenet replanning.", table_cell)
        ]
    ]

    metrics_table = Table(metrics_table_data, colWidths=[135, 95, 292])
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_card_bg]),
        ('PADDING', (0, 0), (-1, -1), 3.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(metrics_table)
    story.append(Spacer(1, 4))

    # =========================================================================
    # 6. MATLAB ONNX INTEGRATION
    # =========================================================================
    story.append(Paragraph("5. Loading & Executing ONNX Models in MATLAB / Simulink", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=1, spaceAfter=4))

    matlab_code_box = Table([[
        Paragraph(
            "<font color='#007ACC'>% =========================================================<br/>"
            "% MATLAB COMMAND WINDOW / SCRIPT: LOADING TRAINED AI MODELS<br/>"
            "% =========================================================</font><br/>"
            "<font color='#007ACC'>% 1. Import Trained 2D YOLOv8 Detector into MATLAB Deep Learning Toolbox</font><br/>"
            "net_yolo = importONNXNetwork('d:/SIH2026/training_suite/best.onnx');<br/><br/>"
            "<font color='#007ACC'>% 2. Import Multi-Agent Trajectory Prediction Neural Network</font><br/>"
            "net_trajectory = importONNXNetwork('d:/SIH2026/training_suite/trajectory_predictor.onnx');<br/><br/>"
            "<font color='#007ACC'>% 3. Real-time Closed-Loop Perception & Prediction Loop</font><br/>"
            "cameraFrame = getCameraImage(egoVehicle); &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<font color='#007ACC'>% 3D Synthetic / Real Frame</font><br/>"
            "detections = predict(net_yolo, cameraFrame); &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<font color='#007ACC'>% YOLO Inference (Auto/Cow/Pothole)</font><br/>"
            "futurePaths = predict(net_trajectory, pastHistory); &nbsp;&nbsp;<font color='#007ACC'>% 1-3s Motion Forecast for Frenet Planner</font>",
            code_block_style
        )
    ]], colWidths=[522])
    matlab_code_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(matlab_code_box)
    story.append(Spacer(1, 4))

    # =========================================================================
    # 7. GOOGLE COLAB FREE GPU TIP & TROUBLESHOOTING
    # =========================================================================
    story.append(Paragraph("6. Google Colab Cloud GPU Training & Best Practices", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=1, spaceAfter=4))

    story.append(Paragraph("• <b>Zero-Install Cloud Training (Google Colab / Kaggle):</b> If you prefer not to load your laptop GPU, use Google Colab with free NVIDIA T4 (16GB VRAM) for 5x faster training. Download generated <code>best.onnx</code> directly.", bullet_style))
    story.append(Paragraph("• <b>Local Laptop GPU Optimization (RTX 2050 4GB):</b> Set <code>batch=16</code> for YOLOv8n/s, or <code>batch=8</code> for YOLOv8m to prevent CUDA Out-of-Memory (OOM).", bullet_style))
    story.append(Paragraph("• <b>Real-time Inference Speed:</b> Ensure per-frame compute latency is under 15ms to satisfy MathWorks 50Hz closed-loop control requirement.", bullet_style))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"AI Model Training Guide PDF successfully generated at: {output_pdf_path}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "d:/SIH2026/SIH2026_AI_Model_Training_Guide.pdf"
    build_training_pdf(out_file)
