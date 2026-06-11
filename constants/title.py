def _hex(value):
    value = value.lstrip("#")
    return (int(value[0:2], 16), int(value[2:4], 16), int(value[4:6], 16))


LOGO_OUTLINE   = _hex("#0a0c05")
ROT_ORANGE     = _hex("#f3851b")
ROT_ORANGE_HI  = _hex("#ffb24a")
ROT_ORANGE_SH  = _hex("#a8540a")
OOZE_GREEN     = _hex("#9bd227")
OOZE_GREEN_HI  = _hex("#caf25a")
OOZE_GREEN_SH  = _hex("#4f7d18")
CLEANER_CYAN   = _hex("#3CA0E0")
CLEANER_CYAN_HI = _hex("#BFE0F4")
CLEANER_CYAN_SH = _hex("#0E1B26")
BLOOD          = _hex("#e23b4e")
BLOOD_DARK     = _hex("#7a1410")

BOTTLE_LEGEND = {
    "o": LOGO_OUTLINE,
    "c": CLEANER_CYAN,
    "h": CLEANER_CYAN_HI,
    "d": CLEANER_CYAN_SH,
}

SKY_TOP    = _hex("#2b3a1c")
SKY_MID    = _hex("#18200f")
SKY_BOTTOM = _hex("#090c06")
MOON_CORE  = _hex("#c6dc6a")
MOON_CRATER = _hex("#9cb24e")
MOON_GLOW  = (182, 216, 74)
BUILDING   = _hex("#0e150a")
BUILDING_BROKEN = _hex("#0a0d07")
WINDOW_DARK = _hex("#141b0c")
WINDOW_LIT  = _hex("#b6e84a")
GROUND      = _hex("#0a0d07")
GROUND_SPECK = _hex("#11180b")
MOUND       = _hex("#0c1208")
LITTER_COLORS = [_hex(c) for c in ("#c8631a", "#8a9a3e", "#9aa6b0", "#b4452c", "#cdb24a")]
ASH_COLOR   = _hex("#828d5c")
FLY_COLOR   = _hex("#05060a")

PLAQUE_FILL    = _hex("#171204")
PLAQUE_BORDER  = _hex("#f4c83a")
PLAQUE_INNER   = _hex("#0a0c05")
PLAQUE_RIVET_SH = _hex("#8a6a14")
PLAQUE_TEXT    = _hex("#f4c83a")

BADGE_CREAM = _hex("#f2e7d4")
BADGE_RED   = _hex("#d22a2a")
BADGE_DARK  = _hex("#1c1c1c")

CREDIT_LABEL_COLOR = _hex("#7f8a5a")
CREDIT_NAME_COLOR  = _hex("#e7ddc8")

WINDOW_BG = _hex("#07080c")

# hand-built 5x7 pixel font — source glyphs for the logotype and the PRESS START plaque
TITLE_FONT = {
    "T": ["11111", "00100", "00100", "00100", "00100", "00100", "00100"],
    "R": ["11110", "10001", "10001", "11110", "10100", "10010", "10001"],
    "A": ["01110", "10001", "10001", "11111", "10001", "10001", "10001"],
    "S": ["01111", "10000", "10000", "01110", "00001", "00001", "11110"],
    "H": ["10001", "10001", "10001", "11111", "10001", "10001", "10001"],
    "Y": ["10001", "10001", "01010", "00100", "00100", "00100", "00100"],
    "P": ["11110", "10001", "10001", "11110", "10000", "10000", "10000"],
    "O": ["01110", "10001", "10001", "10001", "10001", "10001", "01110"],
    "C": ["01111", "10000", "10000", "10000", "10000", "10000", "01111"],
    "L": ["10000", "10000", "10000", "10000", "10000", "10000", "11111"],
    "E": ["11111", "10000", "10000", "11110", "10000", "10000", "11111"],
    "N": ["10001", "11001", "10101", "10101", "10011", "10001", "10001"],
    "D": ["11110", "10001", "10001", "10001", "10001", "10001", "11110"],
    "G": ["01110", "10001", "10000", "10111", "10001", "10001", "01110"],
    "U": ["10001", "10001", "10001", "10001", "10001", "10001", "01110"],
    "M": ["10001", "11011", "10101", "10101", "10001", "10001", "10001"],
    "Q": ["01110", "10001", "10001", "10001", "10101", "10010", "01101"],
    "I": ["11111", "00100", "00100", "00100", "00100", "00100", "11111"],
}

# hand-authored spray bottle, 13x21 cells — stands in for the "A" of TRASHY
TITLE_BOTTLE = [
    "..ooooo......",
    ".ohhccooooo..",
    ".ohccccccccdo",
    ".ohccccoooo..",
    ".ohccccodd...",
    ".oohccoo..d..",
    "..ohcco...d..",
    "..ohcco...d..",
    "..ohcco..d...",
    "..ohcco......",
    ".ohccccccco..",
    "ohcccccccccdo",
    "ohchhhhhhccdo",
    "ohchdhhdhccdo",
    "ohchhddhhccdo",
    "ohchhhhhhccdo",
    "ohcccccccccdo",
    "ohcccccccccdo",
    "ohcccccccccdo",
    "odddddddddddo",
    ".ooooooooooo.",
]

# design-space layout (authored against the 1000 x 600 reference)
TITLE_REF_WIDTH  = 1000
TITLE_REF_HEIGHT = 600

BG_GRID_WIDTH  = 320
BG_GRID_HEIGHT = 192

LOGO_GRID_WIDTH  = 130
LOGO_GRID_HEIGHT = 60
LOGO_BOX_LEFT   = 240
LOGO_BOX_TOP    = 56
LOGO_BOX_WIDTH  = 520
LOGO_BOX_HEIGHT = 240

PLAQUE_TOP = 354
BADGE_BOTTOM = 30
BADGE_LEFT   = 40
BADGE_DISPLAY = 54

CREDIT_FONT_PATH = "assets/fonts/VT323-Regular.ttf"
CREDIT_FONT_NAME = "VT323"
