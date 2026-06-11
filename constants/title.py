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
    "V": ["10001", "10001", "10001", "10001", "10001", "01010", "00100"],
    "K": ["10001", "10010", "10100", "11000", "10100", "10010", "10001"],
    "W": ["10001", "10001", "10001", "10101", "10101", "10101", "01010"],
    "B": ["11110", "10001", "10001", "11110", "10001", "10001", "11110"],
}

GO_SKY_TOP     = _hex("#241f16")
GO_SKY_MID     = _hex("#15110c")
GO_SKY_BOTTOM  = _hex("#070605")
GO_MOON_CORE   = _hex("#aaa091")
GO_MOON_CRATER = _hex("#82796b")
GO_MOON_GLOW   = (150, 140, 120)
GO_BUILDING    = _hex("#0c0b08")
GO_BUILDING_BROKEN = _hex("#070605")
GO_WINDOW_DARK = _hex("#100d09")
GO_WINDOW_LIT  = _hex("#8a5a2a")
GO_GROUND      = _hex("#070605")
GO_GROUND_SPECK = _hex("#0d0b07")
GO_MOUND       = _hex("#0a0805")
GO_LITTER_COLORS = [_hex(c) for c in ("#7a3a12", "#5a663a", "#5a626c", "#6a2a1c", "#7d6a2a")]
GO_ASH_COLOR   = _hex("#6a6450")
GO_FLY_COLOR   = _hex("#05040a")

GO_WASH_COLOR  = (90, 8, 12)
GO_WASH_ALPHA  = 0.34

GO_PLAQUE_FILL   = _hex("#1a0606")
GO_PLAQUE_BORDER = _hex("#e23b4e")
GO_PLAQUE_INNER  = _hex("#06060a")
GO_PLAQUE_RIVET_SH = _hex("#7a1410")
GO_PLAQUE_TEXT   = _hex("#e23b4e")

GO_TITLE_COLOR    = _hex("#e23b4e")
GO_TITLE_SHADOW   = _hex("#5c0c14")
GO_TITLE_SHADOW2  = _hex("#06060a")

GO_SCORE_LABEL   = _hex("#c14752")
GO_SCORE_VALUE   = _hex("#ff5a5f")
GO_SCORE_BORDER  = (226, 59, 78, 102)
GO_SCORE_DIVIDER = (226, 59, 78, 46)

GO_BG            = _hex("#0a0907")

RESTART_TOP = 466
GAMEOVER_TEXT_TOP = 212
SCOREBOARD_TOP = 300
SCOREBOARD_WIDTH = 360

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
