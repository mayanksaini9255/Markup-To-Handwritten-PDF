# note_generator.py
import os
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle

# --- 1. Define Constants, Paths, and Colors ---
PAGE_WIDTH, PAGE_HEIGHT = A4
MARGIN_TOP = 20*mm; MARGIN_BOTTOM = 20*mm; MARGIN_LEFT = 15*mm; MARGIN_RIGHT = 15*mm
COLUMN_GAP = 10*mm; USABLE_WIDTH = PAGE_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
COLUMN_WIDTH = (USABLE_WIDTH - COLUMN_GAP) / 2; COL1_START_X = MARGIN_LEFT
COL2_START_X = MARGIN_LEFT + COLUMN_WIDTH + COLUMN_GAP
FONT_MAIN_PATH = 'main.ttf'; FONT_SUB_PATH = 'sub.ttf'; FONT_MAIN_NAME = 'MainHeadingFont'; FONT_SUB_NAME = 'SubTextFont'
MAIN_TITLE_SIZE = 38; SUB_TITLE_SIZE = 18; BODY_TEXT_SIZE = 11
COLOR_TEXT = colors.HexColor('#333333'); COLOR_SUB_HIGHLIGHT = colors.Color(220/255, 210/255, 255/255, alpha=0.6)
COLOR_DIVIDER = colors.Color(0.75, 0.75, 0.75); COLOR_BOX_OUTLINE = colors.HexColor('#555555'); COLOR_BOX_FILL = colors.Color(245/255, 245/255, 245/255, alpha=0.5)
COLOR_HIGHLIGHT_TEXT = colors.teal; HIGHLIGHT_PADDING = 1.5*mm; BOX_PADDING = 3*mm
SPACE_AFTER_MAIN_TITLE = 8*mm; SPACE_AFTER_SUB_TITLE = 4*mm; SPACE_BETWEEN_POINTS = 2*mm; SPACE_AROUND_BOX = 5*mm

# --- Font Registration Flag ---
fonts_registered = False

# --- Register Fonts Function ---
def register_fonts():
    global fonts_registered
    if fonts_registered: return
    if not os.path.exists(FONT_MAIN_PATH): print(f"ERROR: Font file not found at '{FONT_MAIN_PATH}'"); exit()
    if not os.path.exists(FONT_SUB_PATH): print(f"ERROR: Font file not found at '{FONT_SUB_PATH}'"); exit()
    try:
        pdfmetrics.registerFont(TTFont(FONT_MAIN_NAME, FONT_MAIN_PATH))
        pdfmetrics.registerFont(TTFont(FONT_SUB_NAME, FONT_SUB_PATH))
        fonts_registered = True
        print("Fonts registered successfully.")
    except Exception as e: print(f"ERROR: Failed to register fonts. Error: {e}"); exit()

# --- Get Paragraph Styles Function ---
def get_paragraph_styles():
    styles = getSampleStyleSheet()
    body_style = ParagraphStyle( name='BodyStyle', parent=styles['Normal'], fontName=FONT_SUB_NAME, fontSize=BODY_TEXT_SIZE, leading=BODY_TEXT_SIZE * 1.4, textColor=COLOR_TEXT,)
    sub_title_style = ParagraphStyle( name='SubTitleStyle', parent=body_style, fontName=FONT_SUB_NAME, fontSize=SUB_TITLE_SIZE, leading=SUB_TITLE_SIZE * 1.4,)
    main_title_style = ParagraphStyle( name='MainTitleStyle', parent=styles['Normal'], fontName=FONT_MAIN_NAME, fontSize=MAIN_TITLE_SIZE, leading=MAIN_TITLE_SIZE * 1.2, textColor=COLOR_TEXT, alignment=1)
    box_text_style = ParagraphStyle( name='BoxTextStyle', parent=body_style, fontSize=BODY_TEXT_SIZE * 0.95, leading=BODY_TEXT_SIZE * 1.4 * 0.95)
    return body_style, sub_title_style, main_title_style, box_text_style

# --- Drawing Helper Functions ---

def estimate_height(element_type, text, available_width, styles):
    body_style, sub_title_style, main_title_style, box_text_style = styles; temp_style = body_style; h_est = 0
    dummy_canvas = canvas.Canvas("dummy.pdf") # Create dummy canvas for wrap calculation
    try:
        if element_type == 'main_title': temp_style = main_title_style; p_temp = Paragraph(text, temp_style); _, h = p_temp.wrapOn(dummy_canvas, USABLE_WIDTH, 10000); h_est = h + SPACE_AFTER_MAIN_TITLE
        elif element_type == 'sub_title': temp_style = sub_title_style; p_temp = Paragraph(text, temp_style); _, h = p_temp.wrapOn(dummy_canvas, available_width, 10000); h_est = h + SPACE_AFTER_SUB_TITLE
        elif element_type == 'box': temp_style = box_text_style; p_temp = Paragraph(text, temp_style); _, h = p_temp.wrapOn(dummy_canvas, available_width - 2*BOX_PADDING, 10000); h_est = h + 2*BOX_PADDING + SPACE_AROUND_BOX * 2
        elif element_type == 'point': bullet_char = "->"; bullet_text = f"{bullet_char} "; dummy_canvas.setFont(temp_style.fontName, temp_style.fontSize); bullet_width = dummy_canvas.stringWidth(bullet_text, temp_style.fontName, temp_style.fontSize); indent = bullet_width + 1.5*mm; text_available_width = available_width - indent; p_temp = Paragraph(text, temp_style); _, h = p_temp.wrapOn(dummy_canvas, text_available_width, 10000); h_est = h + SPACE_BETWEEN_POINTS
        else: p_temp = Paragraph(text, temp_style); _, h = p_temp.wrapOn(dummy_canvas, available_width, 10000); h_est = h
    finally:
        # Ensure dummy file is removed even if errors occur during estimation
        try: os.remove("dummy.pdf")
        except OSError: pass
    return h_est

def draw_main_title(c, text, start_y, main_title_style):
    p = Paragraph(text, main_title_style); w, h = p.wrapOn(c, USABLE_WIDTH, 1000); para_x = MARGIN_LEFT; para_y = start_y - h; p.drawOn(c, para_x, para_y); return h

def draw_sub_title(c, text, start_x, start_y, available_width, sub_title_style):
    p = Paragraph(text, sub_title_style); _, h = p.wrapOn(c, available_width, 1000); actual_text_width = c.stringWidth(text, sub_title_style.fontName, sub_title_style.fontSize); highlight_x = start_x - HIGHLIGHT_PADDING; highlight_y = start_y - h; highlight_width = actual_text_width + 2 * HIGHLIGHT_PADDING; highlight_height = h; c.setFillColor(COLOR_SUB_HIGHLIGHT); c.rect(highlight_x, highlight_y, highlight_width, highlight_height, fill=1, stroke=0); c.setFont(sub_title_style.fontName, sub_title_style.fontSize); c.setFillColor(sub_title_style.textColor); baseline_y = highlight_y + h * 0.15; c.drawString(start_x, baseline_y, text); return h

def draw_wrapped_text(c, text, start_x, start_y, available_width, style, bullet_char=None):
    full_text = text; indent = 0;
    if bullet_char: bullet_text = f"{bullet_char} "; c.setFont(style.fontName, style.fontSize); bullet_width = c.stringWidth(bullet_text, style.fontName, style.fontSize); indent = bullet_width + 1.5*mm; c.setFillColor(style.textColor); bullet_draw_y = start_y - style.leading * 0.85; c.drawString(start_x, bullet_draw_y, bullet_text);
    text_start_x = start_x + indent; text_available_width = available_width - indent; p = Paragraph(full_text, style); w, h = p.wrapOn(c, text_available_width, 1000); p.drawOn(c, text_start_x, start_y - h); return h

def draw_box(c, text, start_x, start_y, available_width, box_text_style):
    text_width_inside = available_width - 2 * BOX_PADDING; p = Paragraph(text, box_text_style); w, text_h = p.wrapOn(c, text_width_inside, 1000); box_height = text_h + 2 * BOX_PADDING; box_width = available_width; box_x = start_x; box_y = start_y - box_height; c.setFillColor(COLOR_BOX_FILL); c.setStrokeColor(COLOR_BOX_OUTLINE); c.setLineWidth(0.5); c.rect(box_x, box_y, box_width, box_height, fill=1, stroke=1); text_draw_x = box_x + BOX_PADDING; text_draw_y = box_y + BOX_PADDING; p.drawOn(c, text_draw_x, text_draw_y); return box_height

def draw_column_divider(c, top_y):
    divider_x = MARGIN_LEFT + COLUMN_WIDTH + COLUMN_GAP / 2; c.setStrokeColor(COLOR_DIVIDER); c.setLineWidth(0.5); c.line(divider_x, top_y, divider_x, MARGIN_BOTTOM)

# --- Parser Function ---
def parse_markup(markup_text):
    elements = []; lines = markup_text.strip().split('\n'); in_box = False; box_content = []
    for line in lines:
        stripped_line = line.strip();
        if not stripped_line: continue
        if in_box:
            if stripped_line == '[/BOX]': in_box = False; elements.append(('box', '\n'.join(box_content))); box_content = []
            else: box_content.append(line)
            continue
        if stripped_line.startswith('[MAIN_TITLE]') and stripped_line.endswith('[/MAIN_TITLE]'): elements.append(('main_title', stripped_line[len('[MAIN_TITLE]'):-len('[/MAIN_TITLE]')].strip()))
        elif stripped_line.startswith('[SUB_TITLE]') and stripped_line.endswith('[/SUB_TITLE]'): elements.append(('sub_title', stripped_line[len('[SUB_TITLE]'):-len('[/SUB_TITLE]')].strip()))
        elif stripped_line.startswith('[POINT:') and ']' in stripped_line:
            try: parts = stripped_line.split(']', 1); symbol = parts[0][len('[POINT:'):].strip(); text = parts[1].strip(); elements.append(('point', symbol, text))
            except IndexError: print(f"WARNING: Malformed [POINT:] tag: {stripped_line}")
        elif stripped_line == '[BOX]': in_box = True; box_content = []
        elif stripped_line == '[COLUMN_BREAK]': elements.append(('column_break', ''))
        elif stripped_line == '[PAGE_BREAK]': elements.append(('page_break', ''))
        else: print(f"WARNING: Unrecognized line or tag: {stripped_line}")
    if in_box: print("WARNING: Reached end of input with open [BOX] tag.");
    if box_content: elements.append(('box', '\n'.join(box_content)))
    return elements


# --- THE MAIN PDF GENERATION FUNCTION ---
def generate_pdf_bytes(elements_list):
    """Generates the PDF document into an in-memory bytes buffer."""
    register_fonts()
    body_style, sub_title_style, main_title_style, box_text_style = get_paragraph_styles()
    all_styles = (body_style, sub_title_style, main_title_style, box_text_style)

    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    print("Created PDF canvas in memory.")

    is_first_page = True
    current_x = COL1_START_X
    current_y = PAGE_HEIGHT - MARGIN_TOP
    current_page_start_y = current_y

    def check_and_handle_overflow(c, element_data, current_x, current_y, current_page_start_y):
        nonlocal is_first_page
        el_type = element_data[0]; el_text = "";
        if len(element_data) > 1: el_text = element_data[-1]
        if el_type in ['column_break', 'page_break']: est_h = 0
        else: col_width = COLUMN_WIDTH; est_h = estimate_height(el_type, el_text, col_width, all_styles)

        if current_y - est_h < MARGIN_BOTTOM:
            if current_x == COL1_START_X:
                print(f"--- Switching to Col 2 (Y: {current_y:.1f}, Est H: {est_h:.1f}) ---")
                current_x = COL2_START_X; current_y = current_page_start_y
            else:
                print(f"--- Triggering Page Break (Y: {current_y:.1f}, Est H: {est_h:.1f}) ---")
                c.showPage(); is_first_page = False; current_x = COL1_START_X
                current_y = PAGE_HEIGHT - MARGIN_TOP; current_page_start_y = current_y
                if elements_list: draw_column_divider(c, current_page_start_y)
                print(f"--- New Page Started (Y: {current_y:.1f}) ---")
        return current_x, current_y, current_page_start_y

    if not elements_list:
        print("WARNING: No content elements to draw.")
        c.save(); buffer.seek(0); return buffer.getvalue()

    for index, element in enumerate(elements_list):
        element_type = element[0]

        if element_type == 'column_break':
            if current_x == COL1_START_X: print("--- Manual Column Break ---"); current_x = COL2_START_X; current_y = current_page_start_y
            continue
        if element_type == 'page_break':
             print("--- Manual Page Break ---"); c.showPage(); is_first_page = False; current_x = COL1_START_X
             current_y = PAGE_HEIGHT - MARGIN_TOP; current_page_start_y = current_y
             if index + 1 < len(elements_list): draw_column_divider(c, current_page_start_y)
             continue

        current_x, current_y, current_page_start_y = check_and_handle_overflow(
            c, element, current_x, current_y, current_page_start_y
        )

        consumed_h = 0; current_col_width = COLUMN_WIDTH

        # --- CORRECTED CALLS: Pass the style objects ---
        if element_type == 'main_title':
            if is_first_page:
                text = element[1]; consumed_h = draw_main_title(c, text, current_y, main_title_style) # Pass style
                current_y -= consumed_h; current_y -= SPACE_AFTER_MAIN_TITLE
                consumed_h += SPACE_AFTER_MAIN_TITLE; current_page_start_y = current_y
                draw_column_divider(c, current_page_start_y)
            else:
                 consumed_h = 0
                 if current_y == PAGE_HEIGHT - MARGIN_TOP: draw_column_divider(c, current_y)
        elif element_type == 'sub_title':
            text = element[1]; consumed_h = draw_sub_title(c, text, current_x, current_y, current_col_width, sub_title_style) # Pass style
            current_y -= consumed_h; current_y -= SPACE_AFTER_SUB_TITLE; consumed_h += SPACE_AFTER_SUB_TITLE
        elif element_type == 'point':
             bullet = element[1]; text = element[2]
             consumed_h = draw_wrapped_text(c, text, current_x, current_y, current_col_width, body_style, bullet_char=bullet) # Pass body_style
             current_y -= consumed_h; current_y -= SPACE_BETWEEN_POINTS; consumed_h += SPACE_BETWEEN_POINTS
        elif element_type == 'box':
             text = element[1]; current_y -= SPACE_AROUND_BOX
             consumed_h = draw_box(c, text, current_x, current_y, current_col_width, box_text_style) # Pass style
             current_y -= consumed_h; current_y -= SPACE_AROUND_BOX; consumed_h += SPACE_AROUND_BOX * 2

    c.save()
    print("PDF generation complete in memory buffer.")
    buffer.seek(0); pdf_bytes = buffer.getvalue(); buffer.close()
    return pdf_bytes

# --- Standalone Test Block ---
if __name__ == "__main__":
    print("Running note_generator.py as standalone script...")
    INPUT_FILE = 'input_notes.txt'; OUTPUT_FILE = 'standalone_output.pdf'
    try:
        with open(INPUT_FILE, 'r', encoding='utf-8') as f: test_markup = f.read()
        elements = parse_markup(test_markup)
        if elements:
             pdf_data = generate_pdf_bytes(elements)
             with open(OUTPUT_FILE, 'wb') as out_f: out_f.write(pdf_data)
             print(f"Successfully saved standalone test PDF to '{OUTPUT_FILE}'")
        else: print("No elements parsed, standalone PDF not generated.")
    except FileNotFoundError: print(f"ERROR: Create '{INPUT_FILE}' with markup for standalone testing.")
    except Exception as e: print(f"Error during standalone test: {e}")