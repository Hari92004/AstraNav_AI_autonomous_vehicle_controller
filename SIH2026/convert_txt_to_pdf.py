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
            self.setFillColor(colors.HexColor("#4A5568"))
            self.drawString(54, 11 * inch - 36, "Smart India Hackathon 2026 | Problem Statement ID: 26037")
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
        
        # Footer (all pages)
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.75)
        self.line(54, 46, 8.5 * inch - 54, 46)
        
        self.drawString(54, 32, "Confidential & Academic Use • SIH 2026")
        page_str = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, page_str)
        
        self.restoreState()

def create_problem_statement_pdf(txt_path, output_pdf_path):
    with open(txt_path, 'r', encoding='utf-8', errors='replace') as f:
        raw_text = f.read()

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor("#0F3D64")      # Deep rich navy
    secondary_color = colors.HexColor("#007ACC")    # Vibrant blue accent
    dark_text = colors.HexColor("#1A202C")          # Dark slate
    body_text_color = colors.HexColor("#2D3748")    # Charcoal body text
    bg_light = colors.HexColor("#F8FAFC")           # Off-white / light slate
    callout_bg = colors.HexColor("#EDF2F7")         # Soft slate box
    accent_bar = colors.HexColor("#3182CE")

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#0F3D64"),
        spaceAfter=8
    )

    badge_style = ParagraphStyle(
        'Badge',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=colors.white
    )

    meta_label = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#4A5568")
    )

    meta_val = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=colors.HexColor("#1A202C")
    )

    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#0F3D64"),
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=14,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=8,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'Body_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=body_text_color,
        spaceAfter=5
    )

    bullet_style = ParagraphStyle(
        'Bullet_Custom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=body_text_color,
        leftIndent=14,
        spaceAfter=3
    )

    code_style = ParagraphStyle(
        'Code_Custom',
        parent=styles['Normal'],
        fontName='Courier-Bold',
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#2D3748")
    )

    story = []

    # Parse metadata if present
    lines = raw_text.splitlines()
    
    # Metadata extraction
    ps_id = "26037"
    ps_title = "Adaptive Path Planning and Collision Avoidance for Autonomous Vehicles on Unstructured Indian Roads"
    org = "MathWorks"
    dept = "MathWorks"
    cat = "Software"
    theme = "Robotics and Drones"

    for line in lines:
        if line.startswith("Problem Statement ID:"):
            ps_id = line.split(":", 1)[1].strip()
        elif line.startswith("Title:"):
            ps_title = line.split(":", 1)[1].strip()
        elif line.startswith("Organization:"):
            org = line.split(":", 1)[1].strip()
        elif line.startswith("Department:"):
            dept = line.split(":", 1)[1].strip()
        elif line.startswith("Category:"):
            cat = line.split(":", 1)[1].strip()
        elif line.startswith("Theme:"):
            theme = line.split(":", 1)[1].strip()

    # Header Card
    header_table_data = [
        [
            Paragraph(f"<font color='#FFFFFF'><b>PROBLEM STATEMENT #{ps_id}</b></font>", badge_style),
            Paragraph(f"<font color='#E2E8F0'><b>Theme:</b> {theme} | <b>Category:</b> {cat}</font>", ParagraphStyle('TopRight', parent=badge_style, alignment=2))
        ]
    ]
    header_top = Table(header_table_data, colWidths=[200, 304])
    header_top.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), primary_color),
        ('PADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(header_top)

    # Title Box
    title_data = [
        [
            Paragraph(f"<b>{ps_title}</b>", title_style)
        ],
        [
            Table([
                [
                    Paragraph("<b>Organization:</b>", meta_label), Paragraph(org, meta_val),
                    Paragraph("<b>Department:</b>", meta_label), Paragraph(dept, meta_val),
                ]
            ], colWidths=[80, 160, 80, 160])
        ]
    ]
    title_table = Table(title_data, colWidths=[504])
    title_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F1F5F9")),
        ('LEFTPADDING', (0, 0), (-1, -1), 12),
        ('RIGHTPADDING', (0, 0), (-1, -1), 12),
        ('TOPPADDING', (0, 0), (-1, -1), 10),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 10),
        ('LINEBELOW', (0, -1), (-1, -1), 1.5, secondary_color),
    ]))
    story.append(title_table)
    story.append(Spacer(1, 10))

    # Process Sections
    in_section = False
    arch_block = []
    
    i = 0
    while i < len(lines):
        raw_line = lines[i].rstrip()
        line = raw_line.strip()
        
        # Skip original header lines and footer meta lines
        if any(line.startswith(prefix) for prefix in [
            "Problem Statement ID:", "Title:", "Organization:", "Department:", "Category:", "Theme:"
        ]):
            i += 1
            continue

        # Check for Section Headings like "1. Background", "2. Objective", "10. Expected Deliverables"
        section_match = re.match(r"^(\d+)\.\s+(.*)$", line)
        sub_section_match = re.match(r"^(\d+\.\d+)\s+(.*)$", line)

        if section_match:
            sec_num, sec_title = section_match.groups()
            # Render section header with accent line
            story.append(Spacer(1, 6))
            story.append(Paragraph(f"{sec_num}. {sec_title}", h1_style))
            story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#E2E8F0"), spaceBefore=2, spaceAfter=6))
            i += 1
            continue

        elif sub_section_match:
            sub_num, sub_title = sub_section_match.groups()
            story.append(Paragraph(f"{sub_num} {sub_title}", h2_style))
            i += 1
            continue

        # Check for numbered list like "1. Unmarked village road"
        num_item_match = re.match(r"^(\d+)\.\s+(.+)$", line)
        if num_item_match and not section_match:
            n_idx, n_text = num_item_match.groups()
            story.append(Paragraph(f"<b>{n_idx}.</b> {n_text}", ParagraphStyle('NumList', parent=body_style, fontName='Helvetica-Bold', textColor=primary_color, spaceBefore=4, spaceAfter=2)))
            i += 1
            continue

        # Architecture diagram block
        if "Sensors -> Perception" in line or "-> Behavior Decision" in line or "-> Vehicle Dynamics" in line:
            arch_lines = []
            while i < len(lines) and ("->" in lines[i] or lines[i].strip().startswith("->") or "Sensors" in lines[i]):
                if lines[i].strip():
                    arch_lines.append(lines[i].strip())
                i += 1
            
            box_content = "<br/>".join([f"&nbsp;&nbsp;<b>{al}</b>" for al in arch_lines])
            arch_table = Table([[
                Paragraph(f"<font color='#0F3D64'><b>PIPELINE FLOW:</b></font><br/>{box_content}", code_style)
            ]], colWidths=[504])
            arch_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EDF2F7")),
                ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E1")),
                ('PADDING', (0, 0), (-1, -1), 8),
            ]))
            story.append(Spacer(1, 4))
            story.append(arch_table)
            story.append(Spacer(1, 6))
            continue

        # Bullet point
        if line.startswith("- ") or line.startswith("• "):
            bullet_content = line[2:].strip()
            # Check if has sub-website on next line
            if i + 1 < len(lines) and lines[i+1].strip().startswith("Website:"):
                site_url = lines[i+1].strip()
                bullet_content += f"<br/><font color='#007ACC'><i>{site_url}</i></font>"
                i += 1
            
            # Format bold labels in bullets if any (e.g. "Indian Driving Dataset (IDD):")
            if ":" in bullet_content:
                parts = bullet_content.split(":", 1)
                formatted_bullet = f"<b>{parts[0]}:</b>{parts[1]}"
            else:
                formatted_bullet = bullet_content

            story.append(Paragraph(f"• &nbsp; {formatted_bullet}", bullet_style))
            i += 1
            continue

        # Indented scenario description or general paragraph
        if raw_line.startswith("\t") or raw_line.startswith("   "):
            story.append(Paragraph(f"<i>{line}</i>", ParagraphStyle('SubDesc', parent=body_style, leftIndent=12, textColor=colors.HexColor("#4A5568"))))
            i += 1
            continue

        # Regular non-empty paragraph
        if line:
            # Subtitle headers inside technology stack like "Primary platform:", "Perception and sensor fusion:"
            if line.endswith(":") and len(line) < 45:
                story.append(Paragraph(f"<b>{line}</b>", ParagraphStyle('SubSub', parent=body_style, fontName='Helvetica-Bold', textColor=colors.HexColor("#2C5282"), spaceBefore=4, spaceAfter=2)))
            else:
                story.append(Paragraph(line, body_style))
        
        i += 1

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {output_pdf_path}")

def convert_generic_txt_to_pdf(txt_path, output_pdf_path):
    """Generic text to PDF converter for standard text documents."""
    with open(txt_path, 'r', encoding='utf-8', errors='replace') as f:
        raw_text = f.read()

    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    body_style = ParagraphStyle(
        'GenericBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#1A202C"),
        spaceAfter=4
    )

    story = []
    lines = raw_text.splitlines()
    for line in lines:
        if line.strip():
            # Escape HTML characters safely
            clean_line = line.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            story.append(Paragraph(clean_line, body_style))
        else:
            story.append(Spacer(1, 6))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF: {output_pdf_path}")

if __name__ == "__main__":
    input_file = sys.argv[1] if len(sys.argv) > 1 else "d:/SIH2026/problemstatement.txt"
    output_file = sys.argv[2] if len(sys.argv) > 2 else "d:/SIH2026/problemstatement.pdf"
    
    if os.path.exists(input_file):
        with open(input_file, 'r', encoding='utf-8', errors='replace') as f:
            sample = f.read(500)
        if "Problem Statement" in sample or "1. Background" in sample:
            create_problem_statement_pdf(input_file, output_file)
        else:
            convert_generic_txt_to_pdf(input_file, output_file)
    else:
        print(f"File not found: {input_file}")

