import customtkinter as cutk

# ----------- COLOR PALETTE (Material Design Inspired) -----------
PRIMARY_COLOR = '#1976d2'        # Blue
PRIMARY_COLOR_DARK = '#1565c0'   # Darker Blue
SECONDARY_COLOR = '#43a047'      # Green
ERROR_COLOR = '#e53935'          # Red
WARNING_COLOR = '#ffa726'        # Orange
INFO_COLOR = '#29b6f6'           # Light Blue
BG_LIGHT = '#f4f8fb'
BG_DARK = '#23272e'
CARD_LIGHT = '#fff'
CARD_DARK = '#23272e'
TEXT_DARK = '#23272e'
TEXT_LIGHT = '#fff'
PLACEHOLDER_LIGHT = '#b0bec5'
PLACEHOLDER_DARK = '#bdbdbd'
BORDER_COLOR = '#90caf9'
FOOTER_COLOR = '#bdbdbd'
HOVER_PRIMARY = '#1565c0'
HOVER_ERROR = '#b71c1c'

# ----------- FONTS -----------
# Arabic: "Cairo", "Tajawal". لاتينية: "Segoe UI", "Roboto"
FONT_MAIN = ("Segoe UI", 15)
FONT_TITLE = ("Segoe UI", 18, "bold")
FONT_HEADER = ("Segoe UI", 17, "bold")
FONT_BUTTON = ("Segoe UI", 14, "bold")
FONT_LABEL = ("Segoe UI", 13)
FONT_FOOTER = ("Segoe UI", 10)

# ----------- DYNAMIC COLOR FUNCTIONS -----------
def get_bg_color():
    mode = cutk.get_appearance_mode()
    return BG_DARK if mode == 'Dark' else BG_LIGHT

def get_card_color():
    mode = cutk.get_appearance_mode()
    return CARD_DARK if mode == 'Dark' else CARD_LIGHT

def get_text_color():
    mode = cutk.get_appearance_mode()
    return TEXT_LIGHT if mode == 'Dark' else TEXT_DARK

def get_placeholder_color():
    mode = cutk.get_appearance_mode()
    return PLACEHOLDER_DARK if mode == 'Dark' else PLACEHOLDER_LIGHT

def get_label_color():
    mode = cutk.get_appearance_mode()
    return TEXT_LIGHT if mode == 'Dark' else TEXT_DARK

def get_button_text_color():
    mode = cutk.get_appearance_mode()
    return TEXT_LIGHT if mode == 'Dark' else TEXT_DARK

def get_footer_color():
    return FOOTER_COLOR

def get_header_color():
    mode = cutk.get_appearance_mode()
    return PRIMARY_COLOR_DARK if mode == 'Dark' else PRIMARY_COLOR

def get_button_color():
    mode = cutk.get_appearance_mode()
    return PRIMARY_COLOR_DARK if mode == 'Dark' else PRIMARY_COLOR

def get_error_color():
    return ERROR_COLOR

def get_hover_primary():
    return HOVER_PRIMARY

def get_hover_error():
    return HOVER_ERROR
