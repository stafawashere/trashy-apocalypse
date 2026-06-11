import math
import random

import arcade
from PIL import Image, ImageDraw

from constants import (
    TITLE_FONT,
    TITLE_BOTTLE,
    BOTTLE_LEGEND,
    LOGO_OUTLINE,
    ROT_ORANGE,
    ROT_ORANGE_HI,
    ROT_ORANGE_SH,
    OOZE_GREEN,
    OOZE_GREEN_HI,
    OOZE_GREEN_SH,
    CLEANER_CYAN,
    CLEANER_CYAN_HI,
    CLEANER_CYAN_SH,
    BLOOD,
    BLOOD_DARK,
    SKY_TOP,
    SKY_MID,
    SKY_BOTTOM,
    MOON_CORE,
    MOON_CRATER,
    MOON_GLOW,
    BUILDING,
    BUILDING_BROKEN,
    WINDOW_DARK,
    WINDOW_LIT,
    GROUND,
    GROUND_SPECK,
    MOUND,
    LITTER_COLORS,
    ASH_COLOR,
    FLY_COLOR,
    PLAQUE_FILL,
    PLAQUE_BORDER,
    PLAQUE_INNER,
    PLAQUE_TEXT,
    BADGE_CREAM,
    BADGE_RED,
    BADGE_DARK,
    WINDOW_BG,
    TITLE_REF_WIDTH,
    TITLE_REF_HEIGHT,
    BG_GRID_WIDTH,
    BG_GRID_HEIGHT,
    LOGO_GRID_WIDTH,
    LOGO_GRID_HEIGHT,
    LOGO_BOX_LEFT,
    LOGO_BOX_TOP,
    LOGO_BOX_WIDTH,
    LOGO_BOX_HEIGHT,
)


def _lcg(seed):
    state = {"s": seed}

    def rnd():
        state["s"] = (state["s"] * 1103515245 + 12345) & 0x7FFFFFFF
        return state["s"] / 0x7FFFFFFF

    return rnd


def _lerp_color(a, b, t):
    return (
        int(round(a[0] + (b[0] - a[0]) * t)),
        int(round(a[1] + (b[1] - a[1]) * t)),
        int(round(a[2] + (b[2] - a[2]) * t)),
    )


def _put(px, width, height, x, y, color):
    if 0 <= x < width and 0 <= y < height:
        px[x, y] = (color[0], color[1], color[2], 255)


# ---------- logotype baking (ports buildWord / renderWord / drawBottle) ----------

def _build_word(text, scale, yoffs, gap, seed, stencil=False, erode=False, melt=False, skip=None):
    skip = skip or []
    glyph_w, glyph_h = 5, 7
    letter_w, letter_h = glyph_w * scale, glyph_h * scale
    n = len(text)
    width = n * letter_w + (n - 1) * gap
    height = letter_h + max(yoffs) + 3
    on = [[False] * width for _ in range(height)]
    rnd = _lcg(seed)

    for i, ch in enumerate(text):
        if i in skip:
            continue
        glyph = TITLE_FONT.get(ch)
        if not glyph:
            continue
        x0 = i * (letter_w + gap)
        y0 = yoffs[i % len(yoffs)]
        for gy in range(glyph_h):
            for gx in range(glyph_w):
                if glyph[gy][gx] != "1":
                    continue
                for sy in range(scale):
                    for sx in range(scale):
                        on[y0 + gy * scale + sy][x0 + gx * scale + sx] = True

    if stencil:
        for i, ch in enumerate(text):
            if i in skip:
                continue
            x0 = i * (letter_w + gap)
            y0 = yoffs[i % len(yoffs)]
            y = y0 + letter_h // 2
            for x in range(x0, x0 + letter_w):
                if y - 2 < 0 or y + 2 >= height:
                    continue
                if on[y][x] and on[y - 2][x] and on[y + 2][x]:
                    on[y][x] = False

    if erode:
        drop = []
        for y in range(height):
            for x in range(width):
                if not on[y][x]:
                    continue
                up = y > 0 and on[y - 1][x]
                dn = y < height - 1 and on[y + 1][x]
                lf = x > 0 and on[y][x - 1]
                rt = x < width - 1 and on[y][x + 1]
                is_convex = (not up and not lf) or (not up and not rt) or (not dn and not lf) or (not dn and not rt)
                if is_convex and rnd() < 0.32:
                    drop.append((y, x))
        for y, x in drop:
            on[y][x] = False

    if melt:
        for x in range(width):
            for y in range(height - 1, -1, -1):
                if not on[y][x]:
                    continue
                if y + 1 >= height or not on[y + 1][x]:
                    if rnd() < 0.16:
                        ext = 1 + (1 if rnd() < 0.35 else 0)
                        for e in range(1, ext + 1):
                            if y + e < height:
                                on[y + e][x] = True
                break

    return on, width, height


def _render_word(px, img_w, img_h, word, ox, oy, ramp, seed, speck=False, rim_from=None, overspray=False):
    on, width, height = word
    rnd = _lcg(seed)

    for y in range(-1, height + 1):
        for x in range(-1, width + 1):
            if 0 <= y < height and 0 <= x < width and on[y][x]:
                continue
            near = False
            for dy in range(-1, 2):
                for dx in range(-1, 2):
                    ny, nx = y + dy, x + dx
                    if 0 <= ny < height and 0 <= nx < width and on[ny][nx]:
                        near = True
                        break
                if near:
                    break
            if near:
                _put(px, img_w, img_h, ox + x, oy + y, ramp["out"])

    for y in range(height):
        for x in range(width):
            if not on[y][x]:
                continue
            up = y > 0 and on[y - 1][x]
            dn = y < height - 1 and on[y + 1][x]
            rt = x < width - 1 and on[y][x + 1]
            col = ramp["base"]
            if not up:
                col = ramp["rim"] if (rim_from is not None and x >= rim_from) else ramp["hi"]
            elif not dn:
                col = ramp["sh"]
            elif rim_from is not None and not rt and x >= rim_from:
                col = ramp["rim"]
            elif speck and rnd() < 0.05:
                col = ramp["sh"]
            elif speck and rnd() < 0.03:
                col = ramp["hi"]
            _put(px, img_w, img_h, ox + x, oy + y, col)

    if overspray:
        for y in range(-2, height + 2):
            for x in range(-2, width + 2):
                if 0 <= y < height and 0 <= x < width and on[y][x]:
                    continue
                near1 = near2 = False
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        ny, nx = y + dy, x + dx
                        if not (0 <= ny < height and 0 <= nx < width) or not on[ny][nx]:
                            continue
                        near2 = True
                        if abs(dy) <= 1 and abs(dx) <= 1:
                            near1 = True
                if near2 and not near1 and rnd() < 0.08:
                    _put(px, img_w, img_h, ox + x, oy + y, ramp["base"])


def _bake_logo():
    img = Image.new("RGBA", (LOGO_GRID_WIDTH, LOGO_GRID_HEIGHT), (0, 0, 0, 0))
    px = img.load()
    w, h = LOGO_GRID_WIDTH, LOGO_GRID_HEIGHT

    yo1 = [0, 1, 2, 1, 2, 3]
    word1 = _build_word("TRASHY", 3, yo1, gap=2, seed=9, erode=True, melt=True, skip=[2])
    _render_word(
        px, w, h, word1, 15, 1,
        {"out": LOGO_OUTLINE, "base": ROT_ORANGE, "hi": ROT_ORANGE_HI, "sh": ROT_ORANGE_SH, "rim": OOZE_GREEN_HI},
        seed=21, speck=True, rim_from=68,
    )

    bottle_x, bottle_y = 50, 1 + yo1[2]
    for y, row in enumerate(TITLE_BOTTLE):
        for x, cell in enumerate(row):
            color = BOTTLE_LEGEND.get(cell)
            if color:
                _put(px, w, h, bottle_x + x, bottle_y + y, color)

    rnd = _lcg(41)
    for _ in range(7):
        x = 68 + rnd() * 40
        y = rnd() * 5
        color = CLEANER_CYAN_HI if rnd() < 0.5 else CLEANER_CYAN
        _put(px, w, h, int(x), int(y), color)
    for _ in range(6):
        x = 15 + rnd() * 14
        y = 22 + rnd() * 5
        color = BLOOD if rnd() < 0.5 else BLOOD_DARK
        _put(px, w, h, int(x), int(y), color)

    yo2 = [1, 0, 1, 0, 0, 1, 0, 1, 0, 1]
    word2 = _build_word("APOCALYPSE", 2, yo2, gap=1, seed=5, stencil=True)
    _render_word(
        px, w, h, word2, 10, 31,
        {"out": LOGO_OUTLINE, "base": OOZE_GREEN, "hi": OOZE_GREEN_HI, "sh": OOZE_GREEN_SH, "rim": OOZE_GREEN_HI},
        seed=33, speck=True, overspray=True,
    )

    return arcade.Texture(img)


# ---------- apocalyptic backdrop baking ----------
def _bake_backdrop(buildings, mounds):
    w, h = BG_GRID_WIDTH, BG_GRID_HEIGHT
    img = Image.new("RGBA", (w, h), (0, 0, 0, 255))
    px = img.load()

    for y in range(h):
        t = y / h
        if t < 0.42:
            color = _lerp_color(SKY_TOP, SKY_MID, t / 0.42)
        else:
            color = _lerp_color(SKY_MID, SKY_BOTTOM, (t - 0.42) / 0.58)
        for x in range(w):
            px[x, y] = (color[0], color[1], color[2], 255)

    moon_x, moon_y, moon_r = 284, 24, 16
    for y in range(0, 90):
        for x in range(200, 320):
            d = math.hypot(x - moon_x, y - moon_y)
            if d >= 50:
                continue
            alpha = 0.32 * max(0.0, (50 - d) / 48)
            base = px[x, y]
            px[x, y] = (
                int(base[0] + (MOON_GLOW[0] - base[0]) * alpha),
                int(base[1] + (MOON_GLOW[1] - base[1]) * alpha),
                int(base[2] + (MOON_GLOW[2] - base[2]) * alpha),
                255,
            )

    draw = ImageDraw.Draw(img)
    draw.ellipse([moon_x - moon_r, moon_y - moon_r, moon_x + moon_r, moon_y + moon_r], fill=MOON_CORE)
    for cx, cy, cr in ((moon_x - 7, moon_y - 5, 4), (moon_x + 6, moon_y + 6, 5), (moon_x + 9, moon_y - 7, 3)):
        draw.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=MOON_CRATER)

    for b in buildings:
        draw.rectangle([b["bx"], b["by"], b["bx"] + b["w"] - 1, b["by"] + b["h"] - 1], fill=BUILDING)
        if b["broken"]:
            chunk = math.ceil(b["w"] * 0.45)
            draw.rectangle([b["bx"], b["by"], b["bx"] + chunk - 1, b["by"] + 2], fill=BUILDING_BROKEN)
        for wx, wy, _capable in b["wins"]:
            draw.rectangle([wx, wy, wx + 1, wy + 1], fill=WINDOW_DARK)

    draw.rectangle([0, 150, w - 1, h - 1], fill=GROUND)
    for i in range(0, w, 4):
        gy = 150 + ((i * 7) % 3)
        draw.rectangle([i, gy, i + 1, gy], fill=GROUND_SPECK)

    for m in mounds:
        left = m["x"] - m["w"] / 2
        right = m["x"] + m["w"] / 2
        draw.ellipse([left, 153 - m["h"], right, 153 + m["h"]], fill=MOUND)
        draw.rectangle([left, 153, right, h - 1], fill=MOUND)
        for sx, sy, color in m["specks"]:
            draw.rectangle([int(sx), int(sy), int(sx) + 1, int(sy) + 1], fill=color)

    return arcade.Texture(img)


def _build_backdrop_data():
    rnd = _lcg(7)
    buildings = []
    windows = []
    x = -8
    while x < 332:
        bw = 14 + int(rnd() * 18)
        bh = 24 + int(rnd() * 40)
        by = 150 - bh
        wins = []
        wy = by + 4
        while wy < 146:
            wx = x + 3
            while wx < x + bw - 3:
                if rnd() < 0.42:
                    capable = rnd() < 0.35
                    wins.append((wx, wy, capable))
                    windows.append((wx, wy, capable))
                wx += 5
            wy += 6
        broken = rnd() < 0.4
        buildings.append({"bx": x, "by": by, "w": bw, "h": bh, "wins": wins, "broken": broken})
        x += bw + 2 + int(rnd() * 4)

    mounds = []
    for mx, mw, mh in ((48, 78, 22), (160, 104, 34), (272, 88, 26)):
        specks = []
        for i in range(9):
            sx = mx + (rnd() - 0.5) * mw * 0.8
            sy = 150 + rnd() * (mh - 4)
            color = LITTER_COLORS[(i + int(mx)) % len(LITTER_COLORS)]
            specks.append((sx, sy, color))
        mounds.append({"x": mx, "w": mw, "h": mh, "specks": specks})

    return buildings, windows, mounds


# ---------- producer badge baking ----------

def _bake_badge():
    n = 24
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    px = img.load()
    cx = cy = 11.5

    for y in range(n):
        for x in range(n):
            d = math.hypot(x - cx, y - cy)
            if d <= 11.4:
                color = BADGE_RED if d > 9.1 else BADGE_CREAM
                px[x, y] = (color[0], color[1], color[2], 255)

    draw = ImageDraw.Draw(img)

    def fill(x, y, w, h, color):
        draw.rectangle([x, y, x + w - 1, y + h - 1], fill=color)

    fill(6, 11, 12, 2, BADGE_DARK)
    fill(4, 11, 2, 2, BADGE_DARK)
    fill(6, 10, 1, 4, BADGE_DARK)
    fill(7, 9, 1, 6, BADGE_DARK)
    fill(6, 11, 2, 1, BADGE_CREAM)
    fill(16, 9, 4, 6, BADGE_DARK)
    fill(20, 10, 2, 1, BADGE_DARK)
    fill(20, 13, 2, 1, BADGE_DARK)
    fill(9, 9, 6, 6, BADGE_CREAM)
    fill(11, 9, 2, 6, BADGE_RED)
    fill(9, 11, 6, 2, BADGE_RED)

    return arcade.Texture(img)


# ---------- CRT overlay (scanlines + vignette) ----------

def _bake_crt():
    w, h = TITLE_REF_WIDTH, TITLE_REF_HEIGHT
    small_w, small_h = 200, 120
    vignette = Image.new("L", (small_w, small_h), 0)
    vpx = vignette.load()
    cx, cy = small_w * 0.5, small_h * 0.42
    rx, ry = small_w * 0.7, small_h * 0.6
    for y in range(small_h):
        for x in range(small_w):
            e = math.hypot((x - cx) / rx, (y - cy) / ry)
            if e <= 0.5:
                vpx[x, y] = 0
            else:
                vpx[x, y] = int(min(1.0, (e - 0.5) / 0.5) * 168)
    vignette = vignette.resize((w, h), Image.BILINEAR)

    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    overlay.putalpha(vignette)

    draw = ImageDraw.Draw(overlay)
    scan_alpha = 56
    for y in range(0, h, 4):
        for line in (y + 2, y + 3):
            if line < h:
                draw.line([(0, line), (w - 1, line)], fill=(0, 0, 0, scan_alpha))

    return arcade.Texture(overlay)


# ---------- bitmap text baking (rendered from the 5x7 font) ----------

def _bake_text(text, scale, color, shadow, gap=2):
    glyph_w, glyph_h = 5, 7
    letter_w, letter_h = glyph_w * scale, glyph_h * scale
    width = len(text) * (letter_w + gap) - gap
    height = letter_h + scale
    img = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    px = img.load()

    for i, ch in enumerate(text):
        glyph = TITLE_FONT.get(ch)
        if not glyph:
            continue
        x0 = i * (letter_w + gap)
        for gy in range(glyph_h):
            for gx in range(glyph_w):
                if glyph[gy][gx] != "1":
                    continue
                for sy in range(scale):
                    for sx in range(scale):
                        x, y = x0 + gx * scale + sx, gy * scale + sy
                        _put(px, width, height, x, y + scale, shadow)
                        _put(px, width, height, x, y, color)

    return arcade.Texture(img), width, height


# ---------- baked-asset caches (deterministic, so shared across scenes) ----------

_assets = None
_text_cache = {}


def baked_assets():
    global _assets
    if _assets is None:
        buildings, windows, mounds = _build_backdrop_data()
        _assets = {
            "buildings": buildings,
            "windows": windows,
            "mounds": mounds,
            "backdrop": _bake_backdrop(buildings, mounds),
            "logo": _bake_logo(),
            "badge": _bake_badge(),
            "crt": _bake_crt(),
        }
    return _assets


def baked_text(text, scale, color, shadow, gap=2):
    key = (text, scale, color, shadow, gap)
    if key not in _text_cache:
        _text_cache[key] = _bake_text(text, scale, color, shadow, gap)
    return _text_cache[key]


# ---------- shared scene: the animated apocalyptic stage (backdrop + logo + CRT) ----------

class ApocalypseScene:
    def __init__(self, screen, show_logo=True):
        self.screen = screen
        self.show_logo = show_logo
        self.camera = arcade.Camera2D()
        self.elapsed = 0.0
        self.mouse_x = -1.0
        self.mouse_y = -1.0

        assets = baked_assets()
        self.backdrop_texture = assets["backdrop"]
        self.logo_texture = assets["logo"]
        self.crt_texture = assets["crt"]
        self.windows = assets["windows"]
        self.mounds = assets["mounds"]

        self._init_ash()
        self._init_backdrop_flies()
        self._init_fx()

        arcade.set_background_color(WINDOW_BG)

    # ---- composition transform (centered, uniformly scaled 1000x600 stage) ----

    @property
    def comp_scale(self):
        return self.screen.scale

    @property
    def comp_left(self):
        return (self.screen.width - TITLE_REF_WIDTH * self.comp_scale) / 2

    @property
    def comp_bottom(self):
        return (self.screen.height - TITLE_REF_HEIGHT * self.comp_scale) / 2

    def design_rect(self, left, top, width, height):
        scale = self.comp_scale
        screen_left = self.comp_left + left * scale
        screen_bottom = self.comp_bottom + (TITLE_REF_HEIGHT - (top + height)) * scale
        return arcade.LBWH(screen_left, screen_bottom, width * scale, height * scale)

    def bg_rect(self, bx, by, w, h):
        cell = TITLE_REF_WIDTH / BG_GRID_WIDTH
        return self.design_rect(bx * cell, by * cell, w * cell, h * cell)

    def logo_rect(self, fx, fy, w, h):
        cell = LOGO_BOX_WIDTH / LOGO_GRID_WIDTH
        return self.design_rect(LOGO_BOX_LEFT + fx * cell, LOGO_BOX_TOP + fy * cell, w * cell, h * cell)

    # ---- animated state ----

    def _init_ash(self):
        self.ash = []
        for _ in range(50):
            self.ash.append({
                "x": random.uniform(0, BG_GRID_WIDTH),
                "y": random.uniform(0, BG_GRID_HEIGHT),
                "vy": 7 + random.random() * 11,
                "vx": -3 - random.random() * 5,
                "len": 2 + random.random() * 3,
                "a": 0.18 + random.random() * 0.4,
            })

    def _init_backdrop_flies(self):
        self.bg_flies = []
        for i in range(8):
            m = self.mounds[i % 3]
            self.bg_flies.append({
                "cx": m["x"] + (random.random() * 44 - 22),
                "cy": 132 + random.random() * 14,
                "r": 4 + random.random() * 8,
                "sp": 1 + random.random() * 2,
                "ph": random.random() * 6.28,
            })

    def _init_fx(self):
        rnd = _lcg(13)

        def mk(x, oy, col, dk, maxlo, maxhi):
            return {
                "x": x, "oy": oy, "col": col, "dk": dk, "w": 2,
                "len": rnd() * 2, "max": maxlo + rnd() * (maxhi - maxlo),
                "sp": 2 + rnd() * 4, "wait": rnd() * 2.5, "drop": None,
            }

        self.drips = [
            mk(19, 25, BLOOD, BLOOD_DARK, 2, 4),
            mk(53, 23, CLEANER_CYAN, CLEANER_CYAN_SH, 2, 4),
            mk(90, 27, OOZE_GREEN, OOZE_GREEN_SH, 2, 4),
            mk(14, 47, OOZE_GREEN, OOZE_GREEN_SH, 3, 8),
            mk(37, 47, OOZE_GREEN, OOZE_GREEN_SH, 2, 6),
            mk(60, 47, OOZE_GREEN, OOZE_GREEN_SH, 3, 9),
            mk(82, 47, OOZE_GREEN, OOZE_GREEN_SH, 2, 7),
            mk(104, 47, OOZE_GREEN, OOZE_GREEN_SH, 3, 8),
        ]
        self.spray = [{"ph": 0.0}, {"ph": 0.27}, {"ph": 0.55}, {"ph": 0.8}]
        self.fx_flies = [
            {"cx": 24, "cy": 51, "r": 5, "sp": 2.6, "ph": 0.0},
            {"cx": 98, "cy": 50, "r": 6, "sp": 2.1, "ph": 2.4},
        ]

    def advance_backdrop(self, delta_time):
        dt = min(0.05, delta_time)
        self.elapsed += dt

        for p in self.ash:
            p["x"] += p["vx"] * dt * 10
            p["y"] += p["vy"] * dt * 10
            if p["y"] > BG_GRID_HEIGHT:
                p["y"] = -2
                p["x"] = random.uniform(0, BG_GRID_WIDTH)
            if p["x"] < 0:
                p["x"] = BG_GRID_WIDTH

        for f in self.bg_flies:
            f["ph"] += dt * f["sp"] * 3
        for f in self.fx_flies:
            f["ph"] += dt * f["sp"] * 3

        for d in self.drips:
            if d["wait"] > 0:
                d["wait"] -= dt
            elif d["len"] < d["max"]:
                d["len"] += d["sp"] * dt
            elif not d["drop"]:
                d["drop"] = {"y": d["oy"] + d["len"], "v": 4}
            if d["drop"]:
                d["drop"]["v"] += 70 * dt
                d["drop"]["y"] += d["drop"]["v"] * dt
                if d["drop"]["y"] > 60:
                    d["drop"] = None
                    d["len"] = random.random() * 2
                    d["wait"] = 0.7 + random.random() * 2.6

        return dt

    # ---- draw ----

    def draw_backdrop(self):
        arcade.draw_texture_rect(self.backdrop_texture, self.design_rect(0, 0, TITLE_REF_WIDTH, TITLE_REF_HEIGHT), pixelated=True)

        ms = self.elapsed * 1000
        for wx, wy, capable in self.windows:
            if capable and math.sin(ms / 320 + wx * 1.7) > 0.35:
                arcade.draw_rect_filled(self.bg_rect(wx, wy, 2, 2), WINDOW_LIT)

        for p in self.ash:
            color = (ASH_COLOR[0], ASH_COLOR[1], ASH_COLOR[2], int(p["a"] * 255))
            arcade.draw_rect_filled(self.bg_rect(int(p["x"]), int(p["y"]), 1, int(p["len"])), color)

        for f in self.bg_flies:
            fx = f["cx"] + math.cos(f["ph"]) * f["r"]
            fy = f["cy"] + math.sin(f["ph"] * 1.7) * f["r"] * 0.6
            arcade.draw_rect_filled(self.bg_rect(int(fx), int(fy), 1, 1), FLY_COLOR)

    def draw_logo(self):
        arcade.draw_texture_rect(self.logo_texture, self.design_rect(LOGO_BOX_LEFT, LOGO_BOX_TOP, LOGO_BOX_WIDTH, LOGO_BOX_HEIGHT), pixelated=True)

        ft = self.elapsed
        for s in self.spray:
            tt = (ft * 0.85 + s["ph"]) % 1
            tm = tt * 0.85
            x = int(62 + 34 * tm)
            y = int(5 - 11 * tm + 30 * tm * tm)
            arcade.draw_rect_filled(self.logo_rect(x, y, 1, 1), CLEANER_CYAN_HI)
            if int(ft * 8) % 2 == 0:
                arcade.draw_rect_filled(self.logo_rect(x, y + 1, 1, 1), CLEANER_CYAN)

        for d in self.drips:
            length = max(0, int(d["len"]))
            tip = int(d["oy"] + d["len"])
            if length > 0:
                arcade.draw_rect_filled(self.logo_rect(d["x"] + 1, d["oy"], 1, length), d["dk"])
                arcade.draw_rect_filled(self.logo_rect(d["x"], d["oy"], d["w"], length), d["col"])
            arcade.draw_rect_filled(self.logo_rect(d["x"] - 1, tip - 1, d["w"] + 2, 3), d["col"])
            arcade.draw_rect_filled(self.logo_rect(d["x"] + 1, tip, 1, 1), d["dk"])
            if d["drop"]:
                dy = int(d["drop"]["y"])
                arcade.draw_rect_filled(self.logo_rect(d["x"], dy, d["w"], 3), d["col"])
                arcade.draw_rect_filled(self.logo_rect(d["x"] + 1, dy + 3, 1, 1), d["dk"])

        wing = int(ft * 9) % 2 == 0
        for f in self.fx_flies:
            fx = int(f["cx"] + math.cos(f["ph"]) * f["r"])
            fy = int(f["cy"] + math.sin(f["ph"] * 1.7) * f["r"] * 0.5)
            arcade.draw_rect_filled(self.logo_rect(fx, fy, 1, 1), LOGO_OUTLINE)
            if wing:
                arcade.draw_rect_filled(self.logo_rect(fx + 1, fy, 1, 1), LOGO_OUTLINE)

    def draw_crt(self):
        arcade.draw_texture_rect(self.crt_texture, self.design_rect(0, 0, TITLE_REF_WIDTH, TITLE_REF_HEIGHT), pixelated=True)

    def on_resize(self, width, height):
        self.screen.resize(width, height)
        self.camera.match_window(position=True)


# ---------- riveted plaque button with hover-scale (used by menus) ----------

class MenuButton:
    def __init__(self, scene, label, design_top, on_click):
        self.scene = scene
        self.on_click = on_click
        self.texture, self.text_w, self.text_h = baked_text(label, 2, PLAQUE_TEXT, PLAQUE_INNER)
        self.design_top = design_top
        self.hovered = False
        self.hover_scale = 1.0

    def box(self):
        pad_x, pad_y = 24, 13
        box_w = self.text_w + pad_x * 2
        box_h = max(self.text_h, 21) + pad_y * 2
        box_left = (TITLE_REF_WIDTH - box_w) / 2
        return box_left, self.design_top, box_w, box_h

    def hit(self, x, y):
        box_left, box_top, box_w, box_h = self.box()
        rect = self.scene.design_rect(box_left, box_top, box_w, box_h)
        return rect.left <= x <= rect.right and rect.bottom <= y <= rect.top

    def update(self, dt):
        target = 1.07 if self.hovered else 1.0
        self.hover_scale += (target - self.hover_scale) * min(1.0, dt * 14)

    def draw(self):
        box_left, box_top, box_w, box_h = self.box()
        border = 3
        center_x = box_left + box_w / 2
        center_y = box_top + box_h / 2
        hover = self.hover_scale

        def prect(left, top, w, h):
            return self.scene.design_rect(
                center_x + (left - center_x) * hover,
                center_y + (top - center_y) * hover,
                w * hover, h * hover,
            )

        arcade.draw_rect_filled(prect(box_left - border, box_top - border, box_w + border * 2, box_h + border * 2), PLAQUE_BORDER)
        arcade.draw_rect_filled(prect(box_left, box_top, box_w, box_h), PLAQUE_FILL)
        for rx, ry in ((box_left - 3, box_top - 3), (box_left + box_w - 5, box_top - 3),
                       (box_left - 3, box_top + box_h - 5), (box_left + box_w - 5, box_top + box_h - 5)):
            arcade.draw_rect_filled(prect(rx, ry, 8, 8), PLAQUE_BORDER)

        text_left = box_left + (box_w - self.text_w) / 2
        text_top = box_top + (box_h - self.text_h) / 2
        arcade.draw_texture_rect(self.texture, prect(text_left, text_top, self.text_w, self.text_h), pixelated=True)
