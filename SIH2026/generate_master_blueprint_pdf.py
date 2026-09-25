import sys
import os
import re
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically draw header and footer with total page count."""
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
        
        # Top Header (pages after page 1)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#334155"))
            self.drawString(54, 11 * inch - 36, "SIH 2026 | PS ID 26037: Adaptive Autonomous Path Planning (MathWorks)")
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "PROJECT BLUEPRINT & DATASET REPO")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
        
        # Bottom Footer (all pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748B"))
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 44, 8.5 * inch - 54, 44)
        
        self.drawString(54, 30, "MathWorks • Smart India Hackathon 2026 • Team Implementation Guide")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 30, page_str)
        
        self.restoreState()

def build_master_pdf(output_pdf_path):
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=50,
        rightMargin=50,
        topMargin=50,
        bottomMargin=50
    )

    styles = getSampleStyleSheet()

    # Color Palette
    c_primary = colors.HexColor("#0B3954")      # Deep Navy
    c_secondary = colors.HexColor("#087E8B")    # Rich Teal
    c_accent = colors.HexColor("#C81D25")       # Crimson Accent
    c_dark = colors.HexColor("#1E293B")         # Charcoal Dark
    c_body = colors.HexColor("#334155")         # Slate Body
    c_light_bg = colors.HexColor("#F8FAFC")     # Soft White Slate
    c_card_bg = colors.HexColor("#F1F5F9")      # Card Light
    c_link = colors.HexColor("#0284C7")         # Sky Blue Link
    c_border = colors.HexColor("#E2E8F0")

    # Typography Styles
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=16, leading=20,
        textColor=colors.HexColor("#0B3954"), spaceAfter=6
    )

    h1_style = ParagraphStyle(
        'SectionH1', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=12, leading=15,
        textColor=c_primary, spaceBefore=14, spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=10, leading=13,
        textColor=c_secondary, spaceBefore=8, spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark', parent=styles['Normal'],
        fontName='Helvetica', fontSize=9, leading=13,
        textColor=c_body, spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'BulletText', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8.5, leading=12.5,
        textColor=c_body, leftIndent=12, spaceAfter=2.5
    )

    code_block_style = ParagraphStyle(
        'CodeBlock', parent=styles['Normal'],
        fontName='Courier', fontSize=8, leading=11,
        textColor=colors.HexColor("#0F172A")
    )

    table_header = ParagraphStyle(
        'TableHeader', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8.5, leading=11,
        textColor=colors.white
    )

    table_cell = ParagraphStyle(
        'TableCell', parent=styles['Normal'],
        fontName='Helvetica', fontSize=8, leading=11,
        textColor=c_dark
    )

    table_cell_bold = ParagraphStyle(
        'TableCellBold', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8, leading=11,
        textColor=c_primary
    )

    badge_style = ParagraphStyle(
        'BadgeText', parent=styles['Normal'],
        fontName='Helvetica-Bold', fontSize=8.5, leading=11,
        textColor=colors.white
    )

    story = []

    # =========================================================================
    # 1. COVER / BANNER HEADER
    # =========================================================================
    top_bar_data = [
        [
            Paragraph("<b>SMART INDIA HACKATHON 2026 | PROBLEM ID: 26037</b>", badge_style),
            Paragraph("<b>Category:</b> Software &nbsp;|&nbsp; <b>Theme:</b> Robotics & Drones", ParagraphStyle('RightBadge', parent=badge_style, alignment=2))
        ]
    ]
    top_bar = Table(top_bar_data, colWidths=[240, 272])
    top_bar.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_primary),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(top_bar)

    title_box_data = [
        [
            Paragraph("<b>Adaptive Path Planning and Collision Avoidance for Autonomous Vehicles on Unstructured Indian Roads</b>", title_style)
        ],
        [
            Table([
                [
                    Paragraph("<b>Organization:</b>", ParagraphStyle('ML', parent=body_style, fontName='Helvetica-Bold', fontSize=8.5)),
                    Paragraph("MathWorks", ParagraphStyle('MV', parent=body_style, fontSize=8.5)),
                    Paragraph("<b>Department:</b>", ParagraphStyle('ML', parent=body_style, fontName='Helvetica-Bold', fontSize=8.5)),
                    Paragraph("MathWorks Engineering", ParagraphStyle('MV', parent=body_style, fontSize=8.5)),
                ]
            ], colWidths=[80, 170, 80, 170])
        ]
    ]
    title_box = Table(title_box_data, colWidths=[512])
    title_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), c_card_bg),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, -1), (-1, -1), 2, c_secondary),
    ]))
    story.append(title_box)
    story.append(Spacer(1, 8))

    # =========================================================================
    # 2. EXECUTIVE SUMMARY & OBJECTIVE
    # =========================================================================
    story.append(Paragraph("1. Project Executive Summary & Core Objective", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    story.append(Paragraph(
        "Design and simulate an end-to-end closed-loop autonomous driving system capable of real-time perception, multi-agent motion prediction, behavior decision-making, and adaptive collision-free path planning on <b>unstructured Indian roads</b> where standard lane markings are absent, traffic participants (auto-rickshaws, two-wheelers, cyclists, stray cattle, pedestrians) exhibit non-lane behavior, and road conditions feature potholes and uncertain boundaries.",
        body_style
    ))

    # Architecture Callout Box
    arch_box = Table([[
        Paragraph(
            "<b>CLOSED-LOOP SYSTEM PIPELINE:</b><br/>"
            "<b>Sensors</b> (Camera + LiDAR + Radar) &rarr; <b>Perception & Fusion</b> &rarr; <b>Object Tracking & Motion Prediction</b> &rarr; "
            "<b>Behavior Decision (Stateflow)</b> &rarr; <b>Adaptive Local Path Planner (Frenet / TEB)</b> &rarr; <b>Vehicle Controller (MPC / Pure Pursuit)</b> &rarr; "
            "<b>Vehicle Dynamics (Bicycle Model)</b> &rarr; <b>Updated Scenario Observations</b>",
            ParagraphStyle('Arch', parent=code_block_style, fontSize=7.8, leading=11, textColor=c_primary)
        )
    ]], colWidths=[512])
    arch_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EFF6FF")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#93C5FD")),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(Spacer(1, 4))
    story.append(arch_box)
    story.append(Spacer(1, 8))

    # =========================================================================
    # 2. MASTER DATASET DIRECTORY & DOWNLOAD LINKS
    # =========================================================================
    story.append(Paragraph("2. Master Dataset Directory (Direct Links & Details)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))
    story.append(Paragraph("Clickable direct links for all datasets categorized by traffic, animals, humans, and point clouds:", body_style))

    dataset_table_data = [
        [
            Paragraph("Dataset & Type", table_header),
            Paragraph("Classes & Key Features", table_header),
            Paragraph("Size / Format", table_header),
            Paragraph("Official Download Link", table_header)
        ],
        [
            Paragraph("<b>Indian Driving Dataset (IDD)</b><br/><font color='#087E8B'>Primary Indian Roads</font>", table_cell),
            Paragraph("Auto-rickshaws, motorcycles, riders, pedestrians, <b>stray animals</b>, trucks, unstructured road boundaries.", table_cell),
            Paragraph("IDD-Lite: ~15 GB<br/>Full: ~100 GB<br/>YOLO / JSON", table_cell),
            Paragraph("<font color='#0284C7'><u><a href='https://idd.insaan.iiit.ac.in/'>idd.insaan.iiit.ac.in</a></u></font>", table_cell)
        ],
        [
            Paragraph("<b>Roboflow Indian Cattle</b><br/><font color='#C81D25'>Animals on Road</font>", table_cell),
            Paragraph("Cows, stray cattle, buffaloes, dogs, goats on Indian asphalt & dirt roads. Pre-annotated.", table_cell),
            Paragraph("~500 MB – 2 GB<br/>Direct YOLOv8 / YOLO11", table_cell),
            Paragraph("<font color='#0284C7'><u><a href='https://universe.roboflow.com/search?q=indian+cattle'>universe.roboflow.com</a></u></font>", table_cell)
        ],
        [
            Paragraph("<b>Roboflow Road Animals</b><br/><font color='#C81D25'>Stray Animals & Dogs</font>", table_cell),
            Paragraph("Stray dogs, street animals crossing paths, sudden obstacle animal datasets.", table_cell),
            Paragraph("~1 GB<br/>YOLOv8 PyTorch", table_cell),
            Paragraph("<font color='#0284C7'><u><a href='https://universe.roboflow.com/search?q=road+animal+detection'>universe.roboflow.com</a></u></font>", table_cell)
        ],
        [
            Paragraph("<b>nuScenes Dataset</b><br/><font color='#087E8B'>Multi-Sensor Perception</font>", table_cell),
            Paragraph("360° Cameras, 32-beam LiDAR, Radars. Rich 3D bounding boxes & <b>pedestrian tracks</b>.", table_cell),
            Paragraph("Mini: ~4 GB<br/>Full: ~300 GB<br/>nuScenes format", table_cell),
            Paragraph("<font color='#0284C7'><u><a href='https://www.nuscenes.org/download'>nuscenes.org/download</a></u></font>", table_cell)
        ],
        [
            Paragraph("<b>KITTI 3D Vision Benchmark</b><br/><font color='#087E8B'>Camera & LiDAR</font>", table_cell),
            Paragraph("Velodyne HDL-64E LiDAR point clouds, stereo cameras, calibrated 3D labels for cars & pedestrians.", table_cell),
            Paragraph("~12 GB (3D Object Detection)<br/>Bin/Txt", table_cell),
            Paragraph("<font color='#0284C7'><u><a href='https://www.cvlibs.net/datasets/kitti/eval_3dobject.php'>cvlibs.net/kitti</a></u></font>", table_cell)
        ],
        [
            Paragraph("<b>BDD100K Dataset</b><br/><font color='#087E8B'>Crowded Pedestrians</font>", table_cell),
            Paragraph("100,000 driving videos, dense pedestrian crowds, night & rainy weather conditions.", table_cell),
            Paragraph("Images: ~20 GB<br/>Labels: ~100 MB", table_cell),
            Paragraph("<font color='#0284C7'><u><a href='https://bdd-data.berkeley.edu/'>bdd-data.berkeley.edu</a></u></font>", table_cell)
        ],
        [
            Paragraph("<b>Mendeley Indian Traffic</b><br/><font color='#087E8B'>Indian Vehicles</font>", table_cell),
            Paragraph("Real-world Indian mixed traffic photos & video clips (buses, trucks, auto-rickshaws, bikes).", table_cell),
            Paragraph("~2–5 GB<br/>Images/Videos", table_cell),
            Paragraph("<font color='#0284C7'><u><a href='https://data.mendeley.com/search?q=indian+traffic'>data.mendeley.com</a></u></font>", table_cell)
        ],
        [
            Paragraph("<b>Roboflow Pothole Detection</b><br/><font color='#087E8B'>Road Damage & Potholes</font>", table_cell),
            Paragraph("Indian road potholes, cracks, speed breakers, and unmarked road edge anomalies.", table_cell),
            Paragraph("~800 MB<br/>YOLOv8 format", table_cell),
            Paragraph("<font color='#0284C7'><u><a href='https://universe.roboflow.com/search?q=pothole'>universe.roboflow.com</a></u></font>", table_cell)
        ]
    ]

    dataset_table = Table(dataset_table_data, colWidths=[110, 172, 80, 150])
    dataset_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
        ('PADDING', (0, 0), (-1, -1), 4.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(dataset_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 3. PRE-TRAINED MODELS & REPOSITORIES
    # =========================================================================
    story.append(Paragraph("3. Pre-trained Models & Code Repositories", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))

    models_data = [
        [
            Paragraph("Module Domain", table_header),
            Paragraph("Model / Algorithm", table_header),
            Paragraph("GitHub Repo & Documentation Link", table_header),
            Paragraph("Installation & Execution Command", table_header)
        ],
        [
            Paragraph("<b>2D Vision Perception</b>", table_cell_bold),
            Paragraph("<b>YOLOv8 / YOLO11</b><br/>Ultralytics State-of-the-Art", table_cell),
            Paragraph("<font color='#0284C7'><u><a href='https://github.com/ultralytics/ultralytics'>github.com/ultralytics/ultralytics</a></u></font>", table_cell),
            Paragraph("<font color='#0F172A'>pip install ultralytics<br/>yolo detect train data=idd.yaml model=yolov8m.pt epochs=50</font>", table_cell)
        ],
        [
            Paragraph("<b>3D LiDAR Perception</b>", table_cell_bold),
            Paragraph("<b>MMDetection3D</b><br/>PointPillars & CenterPoint", table_cell),
            Paragraph("<font color='#0284C7'><u><a href='https://github.com/open-mmlab/mmdetection3d'>github.com/open-mmlab/mmdetection3d</a></u></font>", table_cell),
            Paragraph("<font color='#0F172A'>pip install openmim<br/>mim install mmdet3d</font>", table_cell)
        ],
        [
            Paragraph("<b>Multi-Object Tracking</b>", table_cell_bold),
            Paragraph("<b>ByteTrack & BoT-SORT</b><br/>Real-time association", table_cell),
            Paragraph("<font color='#0284C7'><u><a href='https://github.com/ifzhang/ByteTrack'>github.com/ifzhang/ByteTrack</a></u></font>", table_cell),
            Paragraph("<font color='#0F172A'>pip install lap<br/>yolo track model=best.pt tracker='bytetrack.yaml'</font>", table_cell)
        ],
        [
            Paragraph("<b>Motion Prediction</b>", table_cell_bold),
            Paragraph("<b>Trajectron++</b><br/>Multi-agent trajectory forecast", table_cell),
            Paragraph("<font color='#0284C7'><u><a href='https://github.com/StanfordASL/Trajectron-plus-plus'>github.com/StanfordASL/Trajectron-plus-plus</a></u></font>", table_cell),
            Paragraph("<font color='#0F172A'>python train.py --eval_every 10 --dataset nuscenes</font>", table_cell)
        ],
        [
            Paragraph("<b>Path Planning & Control</b>", table_cell_bold),
            Paragraph("<b>PythonRobotics</b><br/>Frenet, Hybrid A*, MPC", table_cell),
            Paragraph("<font color='#0284C7'><u><a href='https://github.com/AtsushiSakai/PythonRobotics'>github.com/AtsushiSakai/PythonRobotics</a></u></font>", table_cell),
            Paragraph("<font color='#0F172A'>python frenet_optimal_trajectory.py</font>", table_cell)
        ],
        [
            Paragraph("<b>MATLAB Simulation</b>", table_cell_bold),
            Paragraph("<b>Automated Driving Toolbox</b><br/>Stateflow & DrivingScenario", table_cell),
            Paragraph("<font color='#0284C7'><u><a href='https://www.mathworks.com/products/automated-driving.html'>mathworks.com/automated-driving</a></u></font>", table_cell),
            Paragraph("<font color='#0F172A'>drivingScenarioDesigner<br/>roadrunner</font>", table_cell)
        ]
    ]

    models_table = Table(models_data, colWidths=[95, 115, 150, 152])
    models_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), c_primary),
        ('GRID', (0, 0), (-1, -1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, c_light_bg]),
        ('PADDING', (0, 0), (-1, -1), 4.5),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(models_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 4. MANDATORY TEST SCENARIOS & ROADRUNNER SETUP
    # =========================================================================
    story.append(Paragraph("4. Mandatory Test Scenarios & Simulation Specs", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))

    scenarios = [
        ("Scenario 1: Unmarked Village Road", "Narrow village road with missing boundary lines, oncoming tractor/bus, parked two-wheelers, and occasional pedestrian walking on asphalt edge."),
        ("Scenario 2: Uncontrolled Urban Intersection", "Busy 4-way intersection without traffic lights or standard right-of-way. Vehicles, bikes, and auto-rickshaws cutting across irregularly."),
        ("Scenario 3: Highway Merge with Slow Traffic", "Autonomous vehicle merging or overtaking slow-moving overloaded trucks and auto-rickshaws under uncertain headway gaps."),
        ("Scenario 4: Dense Market Area with Mixed Traffic", "Pedestrians jaywalking, roadside pushcart vendors, parked bicycles, shop-front encroachments, and high lateral movement."),
        ("Scenario 5: Sudden Cattle-Crossing Event", "Cow / stray dog stepping onto the path with low Time-to-Collision (TTC), requiring immediate risk evaluation, local evasion or emergency braking.")
    ]

    for s_title, s_desc in scenarios:
        story.append(Paragraph(f"<b>{s_title}:</b> <font color='#475569'>{s_desc}</font>", bullet_style))

    story.append(Spacer(1, 6))

    # =========================================================================
    # 5. HARDWARE & ENVIRONMENT SETUP GUIDE
    # =========================================================================
    story.append(Paragraph("5. Powerful PC Hardware & Environment Setup Guide", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))

    hw_box = Table([[
        Paragraph(
            "<b>RECOMMENDED HARDWARE SPECIFICATIONS:</b><br/>"
            "• <b>GPU:</b> NVIDIA RTX 3060 / 3080 / 4070 / 4080 / 4090 (Minimum 8GB+ VRAM, recommended 12GB+ for 3D LiDAR & YOLO)<br/>"
            "• <b>CPU:</b> Intel Core i7 / i9 (12th+ Gen) or AMD Ryzen 7 / 9 (8+ Cores for parallel simulation)<br/>"
            "• <b>RAM:</b> 32 GB DDR4/DDR5 (64 GB ideal for point cloud processing & RoadRunner 3D rendering)<br/>"
            "• <b>Storage:</b> 1 TB NVMe SSD (Datasets: IDD ~15-100GB, nuScenes ~50-300GB, BDD100K ~20GB)<br/><br/>"
            "<b>QUICK CONDA & PYTORCH CUDA SETUP SCRIPT:</b><br/>"
            "<font color='#007ACC'># 1. Create Virtual Environment</font><br/>"
            "conda create -n sih2026 python=3.10 -y &amp;&amp; conda activate sih2026<br/>"
            "<font color='#007ACC'># 2. Install PyTorch with CUDA 12.1</font><br/>"
            "pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121<br/>"
            "<font color='#007ACC'># 3. Install Perception, Vision & Tracking Packages</font><br/>"
            "pip install ultralytics opencv-python numpy scipy matplotlib open3d filterpy lap reportlab",
            ParagraphStyle('HW', parent=code_block_style, fontSize=7.5, leading=10.5)
        )
    ]], colWidths=[512])
    hw_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
        ('PADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(hw_box)
    story.append(Spacer(1, 10))

    # =========================================================================
    # 6. EVALUATION METRICS & FINAL DELIVERABLES
    # =========================================================================
    story.append(Paragraph("6. Evaluation Metrics & Deliverables Checklist", h1_style))

    story.append(HRFlowable(width="100%", thickness=1, color=c_border, spaceBefore=2, spaceAfter=6))

    story.append(Paragraph(
        "<b>Evaluation Metrics:</b> (1) Scenario Completion Rate (%), (2) Collision & Near-Collision Counts, (3) Minimum Obstacle Clearance (m), (4) Replanning Latency (ms), (5) Path Smoothness & Jerk (m/s³), (6) Average & Max Lateral Error (m), (7) Emergency Braking Frequency.<br/><br/>"
        "<b>Final Deliverables Checklist:</b><br/>"
        "&nbsp;&nbsp;[&nbsp;&nbsp;] Working closed-loop MATLAB & Simulink simulation pipeline.<br/>"
        "&nbsp;&nbsp;[&nbsp;&nbsp;] 2 Detailed 3D RoadRunner scenes (Village Road + Urban Unmarked Junction).<br/>"
        "&nbsp;&nbsp;[&nbsp;&nbsp;] 5 Validated Indian road scenarios with trajectory plots.<br/>"
        "&nbsp;&nbsp;[&nbsp;&nbsp;] Perception (YOLO + PointPillars) and Tracking models with weights.<br/>"
        "&nbsp;&nbsp;[&nbsp;&nbsp;] Technical Report, Demonstration Video, and Reproducible Source Code.",
        body_style
    ))

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Master Blueprint PDF successfully generated at: {output_pdf_path}")

if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "d:/SIH2026/SIH2026_ProblemStatement_and_Project_Blueprint.pdf"
    build_master_pdf(out_file)
