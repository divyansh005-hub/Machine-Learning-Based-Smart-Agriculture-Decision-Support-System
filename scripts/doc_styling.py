"""Document styling utilities for NIIT University Software Engineering Deliverables.
Provides professional formatting, cover pages, tables, callouts, and academic typography using python-docx.
"""

import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

# Academic Color Palette
COLOR_PRIMARY = RGBColor(27, 77, 62)       # Forest Green #1B4D3E
COLOR_SECONDARY = RGBColor(46, 125, 50)    # Emerald Green #2E7D32
COLOR_DARK = RGBColor(44, 62, 80)          # Slate #2C3E50
COLOR_MUTED = RGBColor(100, 116, 139)      # Gray #64748B
HEX_PRIMARY = "1B4D3E"
HEX_SECONDARY = "2E7D32"
HEX_LIGHT_BG = "F4F6F5"
HEX_BORDER = "CCCCCC"
HEX_HEADER_BG = "1B4D3E"

def set_cell_background(cell, fill_hex):
    """Set background color of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    """Set inner padding for table cell in dxa (1 pt = 20 dxa)."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tcPr.append(tcMar)

def set_table_borders(table, color="D3D3D3", sz="4", val="single"):
    """Apply clean borders to a table."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:left w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
        f'<w:insideV w:val="none"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

def setup_document(doc):
    """Configure default margins and styles."""
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)

    # Configure Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = COLOR_DARK
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(6)

def add_title_page(doc, doc_title, doc_subtitle, deliverable_code):
    """Create a formal NIIT University title/cover page."""
    # Top spacing
    p_top = doc.add_paragraph()
    p_top.paragraph_format.space_before = Pt(36)
    
    # Institution Header
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst = p_inst.add_run("NIIT UNIVERSITY, NEEMRANA\n")
    r_inst.font.name = 'Calibri'
    r_inst.font.size = Pt(16)
    r_inst.font.bold = True
    r_inst.font.color.rgb = COLOR_PRIMARY
    
    r_dept = p_inst.add_run("DEPARTMENT OF COMPUTER SCIENCE & ENGINEERING\n")
    r_dept.font.name = 'Calibri'
    r_dept.font.size = Pt(12)
    r_dept.font.bold = True
    r_dept.font.color.rgb = COLOR_SECONDARY
    
    r_course = p_inst.add_run("B.Tech Computer Science & Engineering | Software Engineering (CSE)")
    r_course.font.name = 'Calibri'
    r_course.font.size = Pt(10)
    r_course.font.color.rgb = COLOR_MUTED

    # Decorative Divider Line
    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_before = Pt(18)
    p_div.paragraph_format.space_after = Pt(24)
    r_div = p_div.add_run("―" * 45)
    r_div.font.color.rgb = COLOR_SECONDARY

    # Deliverable Code
    p_code = doc.add_paragraph()
    p_code.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_code = p_code.add_run(deliverable_code.upper())
    r_code.font.name = 'Calibri'
    r_code.font.size = Pt(11)
    r_code.font.bold = True
    r_code.font.color.rgb = COLOR_SECONDARY

    # Document Title
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(12)
    p_title.paragraph_format.space_after = Pt(8)
    r_title = p_title.add_run(doc_title)
    r_title.font.name = 'Calibri'
    r_title.font.size = Pt(22)
    r_title.font.bold = True
    r_title.font.color.rgb = COLOR_PRIMARY

    # Subtitle
    if doc_subtitle:
        p_sub = doc.add_paragraph()
        p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_sub.paragraph_format.space_after = Pt(36)
        r_sub = p_sub.add_run(doc_subtitle)
        r_sub.font.name = 'Calibri'
        r_sub.font.size = Pt(12)
        r_sub.font.italic = True
        r_sub.font.color.rgb = COLOR_DARK

    # Submission statement
    p_stmt = doc.add_paragraph()
    p_stmt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_stmt.paragraph_format.space_before = Pt(24)
    p_stmt.paragraph_format.space_after = Pt(36)
    r_stmt = p_stmt.add_run(
        "A Project Deliverable Submitted in Partial Fulfillment of the Requirements\n"
        "for the Course in Software Engineering (B.Tech CSE)"
    )
    r_stmt.font.name = 'Calibri'
    r_stmt.font.size = Pt(10.5)
    r_stmt.font.color.rgb = COLOR_MUTED

    # Author & Guide Details Table (Border-less 2 column)
    meta_table = doc.add_table(rows=1, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_table.autofit = False
    meta_table.columns[0].width = Inches(3.2)
    meta_table.columns[1].width = Inches(3.2)

    cell_left = meta_table.cell(0, 0)
    p_l = cell_left.paragraphs[0]
    p_l.add_run("Submitted By (Group 15):\n").bold = True
    p_l.add_run("• Divyansh Bhatt\n")
    p_l.add_run("• Arush Dewangan\n")
    p_l.add_run("• Smera Sharma\n\n")
    p_l.add_run("B.Tech Computer Science & Engineering\nNIIT University, Neemrana")
    p_l.runs[0].font.color.rgb = COLOR_PRIMARY
    for r in p_l.runs:
        r.font.name = 'Calibri'
        r.font.size = Pt(10.5)

    cell_right = meta_table.cell(0, 1)
    p_r = cell_right.paragraphs[0]
    p_r.add_run("Under the Guidance of:\n").bold = True
    p_r.add_run("Dr. Shreyansh Sharma\n").bold = True
    p_r.add_run("Faculty Guide & Assistant Professor\n")
    p_r.add_run("Department of Computer Science & Engineering\n")
    p_r.add_run("NIIT University, Neemrana")
    p_r.runs[0].font.color.rgb = COLOR_PRIMARY
    for r in p_r.runs:
        r.font.name = 'Calibri'
        r.font.size = Pt(10.5)

    # Date & Academic Year at bottom
    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_foot.paragraph_format.space_before = Pt(48)
    r_foot = p_foot.add_run("Academic Year: 2026-2027 | Submission Date: November 2026")
    r_foot.font.name = 'Calibri'
    r_foot.font.size = Pt(10)
    r_foot.font.bold = True
    r_foot.font.color.rgb = COLOR_SECONDARY

    doc.add_page_break()

def add_heading_1(doc, text):
    """Add styled Heading 1 with accent bar."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(15)
    r.font.bold = True
    r.font.color.rgb = COLOR_PRIMARY
    return p

def add_heading_2(doc, text):
    """Add styled Heading 2."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(14)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(13)
    r.font.bold = True
    r.font.color.rgb = COLOR_SECONDARY
    return p

def add_heading_3(doc, text):
    """Add styled Heading 3."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = 'Calibri'
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_DARK
    return p

def add_callout(doc, text, title="NOTE / CRITICAL GUIDELINE"):
    """Add a highlighted callout container."""
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    
    cell = tbl.cell(0, 0)
    set_cell_background(cell, HEX_LIGHT_BG)
    set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
    
    # Left border thick green
    tcPr = cell._tc.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{HEX_PRIMARY}"/>'
        f'<w:top w:val="none"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(3)
    r_t = p.add_run(f"📌 {title}\n")
    r_t.font.name = 'Calibri'
    r_t.font.size = Pt(10.5)
    r_t.font.bold = True
    r_t.font.color.rgb = COLOR_PRIMARY
    
    r_body = p.add_run(text)
    r_body.font.name = 'Calibri'
    r_body.font.size = Pt(10)
    r_body.font.color.rgb = COLOR_DARK

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def add_styled_table(doc, headers, data, col_widths=None):
    """Add a professional academic table with colored headers and zebra striping."""
    table = doc.add_table(rows=len(data) + 1, cols=len(headers))
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table)

    # Format Header Row
    header_row = table.rows[0]
    header_tr = header_row._tr.get_or_add_trPr()
    header_tr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

    for i, title in enumerate(headers):
        cell = header_row.cells[i]
        set_cell_background(cell, HEX_HEADER_BG)
        set_cell_margins(cell, top=140, bottom=140, left=140, right=140)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(title)
        r.font.name = 'Calibri'
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    # Format Data Rows
    for r_idx, row_data in enumerate(data):
        row = table.rows[r_idx + 1]
        bg_color = HEX_LIGHT_BG if r_idx % 2 == 1 else "FFFFFF"
        for c_idx, val in enumerate(row_data):
            cell = row.cells[c_idx]
            if bg_color != "FFFFFF":
                set_cell_background(cell, bg_color)
            set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
            p = cell.paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p.paragraph_format.space_after = Pt(0)
            r = p.add_run(str(val))
            r.font.name = 'Calibri'
            r.font.size = Pt(9.5)
            r.font.color.rgb = COLOR_DARK

    # Apply Column Widths
    if col_widths:
        for row in table.rows:
            for c_idx, w in enumerate(col_widths):
                row.cells[c_idx].width = Inches(w)

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    return table
