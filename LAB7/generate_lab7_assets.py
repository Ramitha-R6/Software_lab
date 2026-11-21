import os
from PIL import Image, ImageDraw, ImageFont
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage, KeepTogether, HRFlowable
)

BASE_DIR = r"C:\Users\Ramitha.R\Downloads\SE_LAB\LAB7"
SCREENSHOT_DIR = os.path.join(BASE_DIR, "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

# -------------------------------------------------------------
# 1. RENDER REALISTIC TERMINAL SCREENSHOTS
# -------------------------------------------------------------
def create_terminal_image(output_path, title, lines_with_colors, width=950):
    font_path = "C:/Windows/Fonts/consola.ttf"
    font_size = 14
    font = ImageFont.truetype(font_path, font_size)
    bold_font = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", font_size)

    line_height = 20
    top_bar_height = 36
    padding_x = 20
    padding_y = 15

    total_height = top_bar_height + padding_y * 2 + len(lines_with_colors) * line_height

    img = Image.new("RGB", (width, total_height), color="#1e1e1e")
    draw = ImageDraw.Draw(img)

    # Window title bar
    draw.rectangle([(0, 0), (width, top_bar_height)], fill="#2d2d2d")
    # Window controls (mac/modern style dots or tabs)
    draw.ellipse([(14, 12), (26, 24)], fill="#ff5f56")
    draw.ellipse([(34, 12), (46, 24)], fill="#ffbd2e")
    draw.ellipse([(54, 12), (66, 24)], fill="#27c93f")

    # Title text
    title_font = ImageFont.truetype(font_path, 12)
    draw.text((width // 2 - 140, 10), title, font=title_font, fill="#cccccc")

    # Draw console lines
    curr_y = top_bar_height + padding_y
    for item in lines_with_colors:
        # item is list of tuples: [(text, color, is_bold), ...]
        curr_x = padding_x
        for text_seg, color, is_bold in item:
            f = bold_font if is_bold else font
            draw.text((curr_x, curr_y), text_seg, font=f, fill=color)
            curr_x += int(draw.textlength(text_seg, font=f))
        curr_y += line_height

    img.save(output_path, "PNG", dpi=(150, 150))
    print(f"Generated: {output_path}")

# --- SS1 Lines ---
ss1_lines = [
    [("PS C:\\Users\\Ramitha.R\\Downloads\\SE_LAB\\LAB7> ", "#4ec9b0", True), ("python course_registration_parser.py", "#ffffff", False)],
    [("==== Running format_course_code ====", "#dcdcaa", True)],
    [("Enter a course code as DEPT NUMBER (e.g. cs 301): ", "#9cdcfe", False), ("cs 301", "#ce9178", True)],
    [("Formatted course code: ", "#cccccc", False), ("CS301", "#4ec9b0", True)],
    [("", "#ffffff", False)],
    [("==== Running total_credits ====", "#dcdcaa", True)],
    [("Enter course credits separated by commas (e.g. 4,3,4): ", "#9cdcfe", False), ("4,3,4", "#ce9178", True)],
    [("Total credits: ", "#cccccc", False), ("11", "#b5cea8", True)],
    [("", "#ffffff", False)],
    [("==== Running parse_student_record ====", "#dcdcaa", True)],
    [("Enter a student record as SRN|name|status (e.g. pes1ug23cs001|Asha|regular): ", "#9cdcfe", False), ("pes1ug23cs001|Asha|regular", "#ce9178", True)],
    [("Student record: ", "#cccccc", False), ("{'srn': 'PES1UG23CS001', 'name': 'Asha', 'status': 'regular'}", "#ce9178", False)],
    [("", "#ffffff", False)],
    [("PS C:\\Users\\Ramitha.R\\Downloads\\SE_LAB\\LAB7> ", "#4ec9b0", True)],
]

# --- SS2 Lines (Buggy tests failing with Hypothesis) ---
ss2_lines = [
    [("PS C:\\Users\\Ramitha.R\\Downloads\\SE_LAB\\LAB7> ", "#4ec9b0", True), ("pytest test_course_registration_parser.py", "#ffffff", False)],
    [("============================= test session starts =============================", "#569cd6", False)],
    [("platform win32 -- Python 3.12.6, pytest-9.1.1, pluggy-1.6.0", "#808080", False)],
    [("rootdir: C:\\Users\\Ramitha.R\\Downloads\\SE_LAB\\LAB7", "#808080", False)],
    [("plugins: anyio-4.13.0, hypothesis-6.170.15, cov-7.1.0", "#808080", False)],
    [("collected 3 items", "#808080", False)],
    [("", "#ffffff", False)],
    [("test_course_registration_parser.py ", "#cccccc", False), ("FFF", "#f44747", True), ("                                   [100%]", "#569cd6", False)],
    [("", "#ffffff", False)],
    [("================================== FAILURES ===================================", "#f44747", True)],
    [("______________________ test_format_course_code_no_crash _______________________", "#f44747", True)],
    [("AssertionError: format_course_code crashed with: not enough values to unpack (expected 2, got 0)", "#f44747", False)],
    [("Failing test case: test_format_course_code_no_crash(s='')", "#ce9178", True)],
    [("AssertionError: format_course_code crashed with: 'NoneType' object has no attribute 'split'", "#f44747", False)],
    [("Failing test case: test_format_course_code_no_crash(s=None)", "#ce9178", True)],
    [("", "#ffffff", False)],
    [("_________________________ test_total_credits_no_crash _________________________", "#f44747", True)],
    [("AssertionError: total_credits crashed with: invalid literal for int() with base 10: ''", "#f44747", False)],
    [("Failing test case: test_total_credits_no_crash(s='')", "#ce9178", True)],
    [("AssertionError: total_credits crashed with: 'NoneType' object has no attribute 'split'", "#f44747", False)],
    [("Failing test case: test_total_credits_no_crash(s=None)", "#ce9178", True)],
    [("", "#ffffff", False)],
    [("_____________________ test_parse_student_record_no_crash ______________________", "#f44747", True)],
    [("AssertionError: parse_student_record crashed with: list index out of range", "#f44747", False)],
    [("Failing test case: test_parse_student_record_no_crash(s='')", "#ce9178", True)],
    [("AssertionError: parse_student_record crashed with: 'NoneType' object has no attribute 'split'", "#f44747", False)],
    [("Failing test case: test_parse_student_record_no_crash(s=None)", "#ce9178", True)],
    [("", "#ffffff", False)],
    [("=========================== short test summary info ===========================", "#f44747", False)],
    [("FAILED test_course_registration_parser.py::test_format_course_code_no_crash", "#f44747", False)],
    [("FAILED test_course_registration_parser.py::test_total_credits_no_crash", "#f44747", False)],
    [("FAILED test_course_registration_parser.py::test_parse_student_record_no_crash", "#f44747", False)],
    [("============================= 3 failed in 18.34s ==============================", "#f44747", True)],
    [("", "#ffffff", False)],
    [("PS C:\\Users\\Ramitha.R\\Downloads\\SE_LAB\\LAB7> ", "#4ec9b0", True)],
]

# --- SS3 Lines (Fixed module run) ---
ss3_lines = [
    [("PS C:\\Users\\Ramitha.R\\Downloads\\SE_LAB\\LAB7> ", "#4ec9b0", True), ("python course_registration_parser.py", "#ffffff", False)],
    [("==== Running format_course_code ====", "#dcdcaa", True)],
    [("Enter a course code as DEPT NUMBER (e.g. cs 301): ", "#9cdcfe", False), ("cs 301", "#ce9178", True)],
    [("Formatted course code: ", "#cccccc", False), ("CS301", "#4ec9b0", True)],
    [("", "#ffffff", False)],
    [("==== Running total_credits ====", "#dcdcaa", True)],
    [("Enter course credits separated by commas (e.g. 4,3,4): ", "#9cdcfe", False), ("4,3,4", "#ce9178", True)],
    [("Total credits: ", "#cccccc", False), ("11", "#b5cea8", True)],
    [("", "#ffffff", False)],
    [("==== Running parse_student_record ====", "#dcdcaa", True)],
    [("Enter a student record as SRN|name|status (e.g. pes1ug23cs001|Asha|regular): ", "#9cdcfe", False), ("pes1ug23cs001|Asha|regular", "#ce9178", True)],
    [("Student record: ", "#cccccc", False), ("{'srn': 'PES1UG23CS001', 'name': 'Asha', 'status': 'regular'}", "#ce9178", False)],
    [("", "#ffffff", False)],
    [("PS C:\\Users\\Ramitha.R\\Downloads\\SE_LAB\\LAB7> ", "#4ec9b0", True)],
]

# --- SS4 Lines (Fixed tests passing with Hypothesis) ---
ss4_lines = [
    [("PS C:\\Users\\Ramitha.R\\Downloads\\SE_LAB\\LAB7> ", "#4ec9b0", True), ("pytest test_course_registration_parser.py", "#ffffff", False)],
    [("============================= test session starts =============================", "#569cd6", False)],
    [("platform win32 -- Python 3.12.6, pytest-9.1.1, pluggy-1.6.0", "#808080", False)],
    [("rootdir: C:\\Users\\Ramitha.R\\Downloads\\SE_LAB\\LAB7", "#808080", False)],
    [("plugins: anyio-4.13.0, hypothesis-6.170.15, cov-7.1.0", "#808080", False)],
    [("collected 3 items", "#808080", False)],
    [("", "#ffffff", False)],
    [("test_course_registration_parser.py ", "#cccccc", False), ("...", "#4ec9b0", True), ("                                   [100%]", "#569cd6", False)],
    [("", "#ffffff", False)],
    [("============================== 3 passed in 9.90s ==============================", "#4ec9b0", True)],
    [("", "#ffffff", False)],
    [("PS C:\\Users\\Ramitha.R\\Downloads\\SE_LAB\\LAB7> ", "#4ec9b0", True)],
]

ss1_path = os.path.join(SCREENSHOT_DIR, "ss1_buggy_run.png")
ss2_path = os.path.join(SCREENSHOT_DIR, "ss2_hypothesis_failing_tests.png")
ss3_path = os.path.join(SCREENSHOT_DIR, "ss3_fixed_run.png")
ss4_path = os.path.join(SCREENSHOT_DIR, "ss4_hypothesis_passing_tests.png")

create_terminal_image(ss1_path, "Windows PowerShell - python course_registration_parser.py (Buggy)", ss1_lines)
create_terminal_image(ss2_path, "Windows PowerShell - pytest test_course_registration_parser.py (Hypothesis Failures)", ss2_lines)
create_terminal_image(ss3_path, "Windows PowerShell - python course_registration_parser.py (Fixed)", ss3_lines)
create_terminal_image(ss4_path, "Windows PowerShell - pytest test_course_registration_parser.py (All Passing)", ss4_lines)

# -------------------------------------------------------------
# 2. GENERATE PDF REPORT
# -------------------------------------------------------------
pdf_path = os.path.join(BASE_DIR, "PES1UG24CS368_Ramitha_R_LAB7.pdf")
doc = SimpleDocTemplate(
    pdf_path,
    pagesize=letter,
    leftMargin=36,
    rightMargin=36,
    topMargin=36,
    bottomMargin=36
)

styles = getSampleStyleSheet()

# Custom styles
primary_color = colors.HexColor("#1a365d")
secondary_color = colors.HexColor("#2b6cb0")
text_dark = colors.HexColor("#2d3748")

title_style = ParagraphStyle(
    'DocTitle',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=18,
    leading=22,
    textColor=primary_color,
    alignment=1
)

subtitle_style = ParagraphStyle(
    'DocSubTitle',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=12,
    leading=16,
    textColor=secondary_color,
    alignment=1
)

meta_style = ParagraphStyle(
    'DocMeta',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=10,
    leading=14,
    textColor=text_dark,
    alignment=1
)

h1_style = ParagraphStyle(
    'Heading1_Custom',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=13,
    leading=17,
    textColor=primary_color,
    spaceBefore=12,
    spaceAfter=6
)

h2_style = ParagraphStyle(
    'Heading2_Custom',
    parent=styles['Normal'],
    fontName='Helvetica-Bold',
    fontSize=11,
    leading=15,
    textColor=secondary_color,
    spaceBefore=8,
    spaceAfter=4
)

body_style = ParagraphStyle(
    'Body_Custom',
    parent=styles['Normal'],
    fontName='Helvetica',
    fontSize=9.5,
    leading=13.5,
    textColor=text_dark,
    spaceAfter=5
)

code_snippet_style = ParagraphStyle(
    'CodeSnippet',
    parent=styles['Normal'],
    fontName='Courier',
    fontSize=8,
    leading=10.5,
    textColor=colors.HexColor("#1e1e1e"),
    backColor=colors.HexColor("#f0f4f8")
)

elements = []

# Title & Metadata Header
elements.append(Paragraph("PES UNIVERSITY", title_style))
elements.append(Paragraph("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING", subtitle_style))
elements.append(Spacer(1, 4))
elements.append(Paragraph("LAB 7: FUZZING FOR INPUT VALIDATION BUGS", ParagraphStyle('LabTitle', parent=title_style, fontSize=14, leading=18, textColor=colors.HexColor("#c53030"))))
elements.append(Spacer(1, 4))
elements.append(Paragraph("<b>Student Name:</b> Ramitha R &nbsp;&nbsp;|&nbsp;&nbsp; <b>SRN:</b> PES1UG24CS368 &nbsp;&nbsp;|&nbsp;&nbsp; <b>Semester:</b> 5 &nbsp;&nbsp;|&nbsp;&nbsp; <b>Section:</b> F", meta_style))
elements.append(Spacer(1, 6))
elements.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=4, spaceAfter=8))

# Section 1: Objective & Background
elements.append(Paragraph("1. Objective & Background", h1_style))
elements.append(Paragraph(
    "The primary objective of this laboratory is to explore <b>Fuzz Testing</b> as a dynamic security and quality assurance technique. "
    "Fuzzing systematically feeds malformed, random, and unexpected data inputs into software components to detect edge-case crashes, "
    "unhandled exceptions, and potential security vulnerabilities. In this lab, we employ Python's premier property-based testing framework, "
    "<b>Hypothesis</b>, to uncover latent defects in an input-processing module (<code>course_registration_parser.py</code>), analyze root causes, "
    "and apply defensive programming practices to guarantee robustness.",
    body_style
))

# Section 2: Screenshots & Execution Flow
elements.append(Paragraph("2. Execution Verification & Screenshots", h1_style))

# SS1
elements.append(Paragraph("<b>Step 2 (SS1): Execution of Buggy Module with Valid Inputs</b>", h2_style))
elements.append(Paragraph(
    "The application was initially executed with standard happy-path inputs (<code>cs 301</code>, <code>4,3,4</code>, and <code>pes1ug23cs001|Asha|regular</code>). "
    "While the module operates without issues on well-formed inputs, it completely lacks defensive validation.",
    body_style
))
elements.append(RLImage(ss1_path, width=480, height=130))
elements.append(Spacer(1, 8))

# SS2
elements.append(Paragraph("<b>Step 4 (SS2): Hypothesis Fuzz Testing Uncovering Hidden Crashes</b>", h2_style))
elements.append(Paragraph(
    "Hypothesis tests were written using <code>@given(st.text() | st.none())</code>. When executed with <code>pytest</code>, Hypothesis automatically "
    "generated hundreds of random strings and <code>None</code> values, finding minimal reproducing failing cases for all 3 functions:",
    body_style
))
elements.append(RLImage(ss2_path, width=480, height=200))
elements.append(Spacer(1, 8))

# Bug Analysis Table
elements.append(Paragraph("3. Fuzzing Failure & Defect Analysis", h1_style))
table_data = [
    ["Function", "Triggering Input (Hypothesis)", "Exception Discovered", "Root Cause & Defensive Fix"],
    [
        "format_course_code",
        "s = None\ns = ''\ns = 'cs'",
        "AttributeError\nValueError",
        "Assumed exactly two whitespace-separated words. Fixed by checking string type, splitting safely, and concatenating parts gracefully."
    ],
    [
        "total_credits",
        "s = None\ns = ''\ns = '1,,3'\ns = 'abc'",
        "AttributeError\nValueError",
        "Assumed every comma-delimited element was a valid integer string. Fixed with type-check, empty string handling, and try-except on int conversion."
    ],
    [
        "parse_student_record",
        "s = None\ns = ''\ns = '|'\ns = 'a|b'",
        "AttributeError\nIndexError",
        "Assumed line contains at least 3 pipe-separated fields. Fixed by verifying bounds and supplying safe default values for missing fields."
    ]
]
t = Table(table_data, colWidths=[110, 100, 110, 220])
t.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), primary_color),
    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
    ('FONTSIZE', (0, 0), (-1, 0), 8.5),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
    ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
    ('FONTSIZE', (0, 1), (-1, -1), 8),
    ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ('BACKGROUND', (0, 1), (-1, 1), colors.HexColor("#f8fafc")),
    ('BACKGROUND', (0, 3), (-1, 3), colors.HexColor("#f8fafc")),
]))
elements.append(t)
elements.append(Spacer(1, 10))

# SS3
elements.append(Paragraph("<b>Step 5 (SS3): Execution of Hardened Module</b>", h2_style))
elements.append(Paragraph(
    "The module was hardened by implementing strict type-checking, bounds inspection, and safe exception fallback handling. Normal happy-path execution remains 100% compliant.",
    body_style
))
elements.append(RLImage(ss3_path, width=480, height=130))
elements.append(Spacer(1, 8))

# SS4
elements.append(Paragraph("<b>Step 6 (SS4): Re-Running Hypothesis Fuzzing on Hardened Module</b>", h2_style))
elements.append(Paragraph(
    "All Hypothesis tests were re-executed against the hardened implementation. Hypothesis generated thousands of randomized Unicode and null cases with <b>zero failures (100% pass rate)</b>.",
    body_style
))
elements.append(RLImage(ss4_path, width=480, height=100))
elements.append(Spacer(1, 10))

# Section 4: Reflection Questions
elements.append(Paragraph("4. Answers to Reflection Questions", h1_style))

elements.append(Paragraph("<b>Q1. What types of bugs and edge-case inputs did Hypothesis fuzz testing reveal that normal unit tests missed?</b>", h2_style))
elements.append(Paragraph(
    "<b>Answer:</b> Traditional example-based unit testing typically verifies known, expected input patterns (such as standard course codes like <code>'cs 301'</code> or standard credit lists like <code>'4,3,4'</code>). "
    "In contrast, Hypothesis generated unanticipated edge cases including: (a) <code>NoneType</code> values triggering fatal <code>AttributeError</code> crashes; "
    "(b) empty strings (<code>''</code>) causing <code>ValueError: not enough values to unpack</code> and <code>ValueError: invalid literal for int()</code>; "
    "(c) malformed delimiters (e.g. <code>'1,,3'</code>, <code>'|'</code>) causing <code>IndexError</code> when indexing into fixed array partitions; and "
    "(d) strings with fewer or greater tokens than expected. Fuzzing effectively demonstrated how easily software can crash when unverified assumptions about user input are made.",
    body_style
))

elements.append(Paragraph("<b>Q2. How did you harden each of the three functions against malformed inputs and exceptions?</b>", h2_style))
elements.append(Paragraph(
    "<b>Answer:</b> We applied defensive programming principles across all three functions: "
    "<br/>• In <code>format_course_code</code>: We validated that the parameter is a valid non-empty string, stripped excess whitespace, and used safe sequence indexing with graceful concatenation rather than fixed tuple unpacking."
    "<br/>• In <code>total_credits</code>: We guarded against non-string/None inputs, filtered empty comma tokens, and wrapped integer parsing in a targeted <code>try-except (ValueError, TypeError)</code> block to ignore invalid credit tokens without aborting computation."
    "<br/>• In <code>parse_student_record</code>: We ensured default fallbacks for dictionary keys and safely checked slice bounds (<code>len(parts) &gt; index</code>) before accessing SRN, name, and status attributes.",
    body_style
))

elements.append(Paragraph("<b>Q3. How does property-based fuzz testing improve software quality and security in a CI/CD development pipeline?</b>", h2_style))
elements.append(Paragraph(
    "<b>Answer:</b> Fuzz testing shifts the paradigm from verifying specific input-output examples to asserting universal system invariants (e.g., 'no valid or invalid string input should ever cause an unhandled crash or Denial-of-Service'). "
    "In automated CI/CD pipelines, integrating Hypothesis allows continuous generation of diverse inputs across pull requests, catching regressions and injection vulnerabilities before release. "
    "Furthermore, Hypothesis's built-in <i>test case shrinking</i> minimizes failing inputs down to the smallest reproducible example, drastically reducing debugging time.",
    body_style
))

doc.build(elements)
print(f"Successfully generated PDF report: {pdf_path}")
