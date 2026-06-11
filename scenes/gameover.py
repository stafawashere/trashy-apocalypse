import math
import random

import arcade

from constants import (
    TITLE_REF_WIDTH,
    TITLE_REF_HEIGHT,
    BG_GRID_WIDTH,
    BG_GRID_HEIGHT,
    GO_WINDOW_LIT,
    GO_ASH_COLOR,
    GO_FLY_COLOR,
    GO_BG,
    GO_PLAQUE_FILL,
    GO_PLAQUE_BORDER,
    GO_PLAQUE_INNER,
    GO_PLAQUE_TEXT,
    GO_TITLE_COLOR,
    GO_TITLE_SHADOW,
    GO_SCORE_LABEL,
    GO_SCORE_VALUE,
    GO_SCORE_BORDER,
    GO_SCORE_DIVIDER,
    RESTART_TOP,
    GAMEOVER_TEXT_TOP,
    SCOREBOARD_TOP,
    SCOREBOARD_WIDTH,
    CREDIT_FONT_PATH,
    CREDIT_FONT_NAME,
)
from scenes.apocalypse import baked_assets, baked_text, baked_glow


GHOST_LOGO_WIDTH = 780
GHOST_LOGO_HEIGHT = 360
GHOST_LOGO_TOP = (TITLE_REF_HEIGHT - GHOST_LOGO_HEIGHT) / 2 - 12

GAMEOVER_SCALE = 6
GAMEOVER_GAP = 7
GAMEOVER_GLOW_COLOR = (240, 64, 84)

LABEL_SCALE = 2
SCORE_VALUE_SIZE = 30
SCOREBOARD_ROW_HEIGHT = 46
SCOREBOARD_PAD_X = 8
VALUE_BASELINE_FRACTION = 0.2


class GameOverScene:
    def __init__(self, screen, on_back, kills=0, high_score=0, audio=None):
        self.screen = screen
        self.on_back = on_back
        self.audio = audio
        self.kills = kills
        self.high_score = high_score
        self.camera = arcade.Camera2D()
        self.elapsed = 0.0
        self.mouse_x = -1.0
        self.mouse_y = -1.0

        assets = baked_assets()
        self.backdrop_texture = assets["dead_backdrop"]
        self.crt_texture = assets["dead_crt"]
        self.ghost_logo_texture = assets["ghost_logo"]
        self.windows = assets["dead_windows"]
        self.mounds = assets["dead_mounds"]

        self.gameover_texture, self.gameover_w, self.gameover_h = baked_text(
            "GAME OVER", GAMEOVER_SCALE, GO_TITLE_COLOR, GO_TITLE_SHADOW, gap=GAMEOVER_GAP
        )
        self.gameover_glow, self.gameover_glow_w, self.gameover_glow_h = baked_glow(
            "GAME OVER", GAMEOVER_SCALE, GAMEOVER_GLOW_COLOR, gap=GAMEOVER_GAP, blur=9, pad=20
        )

        self.restart_texture, self.restart_w, self.restart_h = baked_text(
            "BACK TO MENU", 2, GO_PLAQUE_TEXT, GO_PLAQUE_INNER
        )

        self.hs_label_tex, self.hs_label_w, self.hs_label_h = baked_text(
            "HIGH SCORE", LABEL_SCALE, GO_SCORE_LABEL, (0, 0, 0, 0)
        )
        self.kc_label_tex, self.kc_label_w, self.kc_label_h = baked_text(
            "KILL COUNT", LABEL_SCALE, GO_SCORE_LABEL, (0, 0, 0, 0)
        )

        arcade.load_font(CREDIT_FONT_PATH)
        self.hs_value_text = self._value_text(f"{self.high_score:,}")
        self.kc_value_text = self._value_text(str(self.kills))
        self.hs_value_shadow = self._value_text(f"{self.high_score:,}", GO_TITLE_SHADOW)
        self.kc_value_shadow = self._value_text(str(self.kills), GO_TITLE_SHADOW)

        self._init_ash()
        self._init_flies()

        self.is_hovering_restart = False
        self.restart_hover_scale = 1.0

        arcade.set_background_color(GO_BG)

    def _value_text(self, value, color=GO_SCORE_VALUE):
        return arcade.Text(
            value, 0, 0, color, SCORE_VALUE_SIZE,
            font_name=CREDIT_FONT_NAME, anchor_x="right", anchor_y="center",
        )

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

    def design_point(self, left, top):
        scale = self.comp_scale
        return (
            self.comp_left + left * scale,
            self.comp_bottom + (TITLE_REF_HEIGHT - top) * scale,
        )

    def bg_rect(self, bx, by, w, h):
        cell = TITLE_REF_WIDTH / BG_GRID_WIDTH
        return self.design_rect(bx * cell, by * cell, w * cell, h * cell)

    def _init_ash(self):
        self.ash = []
        for _ in range(50):
            self.ash.append({
                "x": random.uniform(0, BG_GRID_WIDTH),
                "y": random.uniform(0, BG_GRID_HEIGHT),
                "vy": 7 + random.random() * 11,
                "vx": -3 - random.random() * 5,
                "len": 2 + random.random() * 3,
                "a": 0.14 + random.random() * 0.34,
            })

    def _init_flies(self):
        self.bg_flies = []
        for i in range(10):
            m = self.mounds[i % 3]
            self.bg_flies.append({
                "cx": m["x"] + (random.random() * 44 - 22),
                "cy": 132 + random.random() * 14,
                "r": 4 + random.random() * 8,
                "sp": 1 + random.random() * 2,
                "ph": random.random() * 6.28,
            })

    # update 

    def update(self, delta_time):
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

        target = 1.07 if self.is_hovering_restart else 1.0
        self.restart_hover_scale += (target - self.restart_hover_scale) * min(1.0, dt * 14)

    # draw 

    def draw(self):
        self.camera.use()
        self._draw_backdrop()
        self._draw_crt()
        self._draw_ghost_logo()
        self._draw_scoreboard()
        self._draw_restart_plaque()
        self._draw_gameover_text()

    def _draw_backdrop(self):
        arcade.draw_texture_rect(self.backdrop_texture, self.design_rect(0, 0, TITLE_REF_WIDTH, TITLE_REF_HEIGHT), pixelated=True)

        ms = self.elapsed * 1000
        for wx, wy, capable in self.windows:
            if capable and math.sin(ms / 320 + wx * 1.7) > 0.45:
                arcade.draw_rect_filled(self.bg_rect(wx, wy, 2, 2), GO_WINDOW_LIT)

        for p in self.ash:
            color = (GO_ASH_COLOR[0], GO_ASH_COLOR[1], GO_ASH_COLOR[2], int(p["a"] * 255))
            arcade.draw_rect_filled(self.bg_rect(int(p["x"]), int(p["y"]), 1, int(p["len"])), color)

        for f in self.bg_flies:
            fx = f["cx"] + math.cos(f["ph"]) * f["r"]
            fy = f["cy"] + math.sin(f["ph"] * 1.7) * f["r"] * 0.6
            arcade.draw_rect_filled(self.bg_rect(int(fx), int(fy), 1, 1), GO_FLY_COLOR)

    def _draw_ghost_logo(self):
        left = (TITLE_REF_WIDTH - GHOST_LOGO_WIDTH) / 2
        arcade.draw_texture_rect(
            self.ghost_logo_texture,
            self.design_rect(left, GHOST_LOGO_TOP, GHOST_LOGO_WIDTH, GHOST_LOGO_HEIGHT),
            pixelated=True,
        )

    def _draw_gameover_text(self):
        flicker_phase = (self.elapsed % 4.2) / 4.2
        is_dim = (0.48 <= flicker_phase <= 0.50) or (0.72 <= flicker_phase <= 0.74)
        alpha = 150 if is_dim else 255

        center_x = TITLE_REF_WIDTH / 2
        text_left = center_x - self.gameover_w / 2
        glow_left = center_x - self.gameover_glow_w / 2
        glow_top = GAMEOVER_TEXT_TOP - (self.gameover_glow_h - self.gameover_h) / 2

        arcade.draw_texture_rect(
            self.gameover_glow,
            self.design_rect(glow_left, glow_top, self.gameover_glow_w, self.gameover_glow_h),
            pixelated=True, alpha=int(alpha * 0.55),
        )
        arcade.draw_texture_rect(
            self.gameover_texture,
            self.design_rect(text_left, GAMEOVER_TEXT_TOP, self.gameover_w, self.gameover_h),
            pixelated=True, alpha=alpha,
        )

    def _draw_scoreboard(self):
        scale = self.comp_scale
        board_left = (TITLE_REF_WIDTH - SCOREBOARD_WIDTH) / 2
        row_h = SCOREBOARD_ROW_HEIGHT

        arcade.draw_rect_filled(self.design_rect(board_left, SCOREBOARD_TOP, SCOREBOARD_WIDTH, 2), GO_SCORE_BORDER)
        arcade.draw_rect_filled(self.design_rect(board_left, SCOREBOARD_TOP + row_h, SCOREBOARD_WIDTH, 1), GO_SCORE_DIVIDER)
        arcade.draw_rect_filled(self.design_rect(board_left, SCOREBOARD_TOP + row_h * 2 - 2, SCOREBOARD_WIDTH, 2), GO_SCORE_BORDER)

        label_left = board_left + SCOREBOARD_PAD_X
        value_right = board_left + SCOREBOARD_WIDTH - SCOREBOARD_PAD_X

        self._draw_score_row(
            SCOREBOARD_TOP + row_h / 2, label_left, value_right, scale,
            self.hs_label_tex, self.hs_label_w, self.hs_label_h,
            self.hs_value_text, self.hs_value_shadow,
        )
        self._draw_score_row(
            SCOREBOARD_TOP + row_h + row_h / 2, label_left, value_right, scale,
            self.kc_label_tex, self.kc_label_w, self.kc_label_h,
            self.kc_value_text, self.kc_value_shadow,
        )

    def _draw_score_row(self, center_y, label_left, value_right, scale, label_tex, label_w, label_h, value_text, value_shadow):
        arcade.draw_texture_rect(
            label_tex,
            self.design_rect(label_left, center_y - label_h / 2, label_w, label_h),
            pixelated=True,
        )
        value_x, value_y = self.design_point(value_right, center_y)
        baseline_lift = SCORE_VALUE_SIZE * scale * VALUE_BASELINE_FRACTION
        value_shadow.font_size = SCORE_VALUE_SIZE * scale
        value_shadow.x = value_x
        value_shadow.y = value_y + baseline_lift - 2 * scale
        value_shadow.draw()
        value_text.font_size = SCORE_VALUE_SIZE * scale
        value_text.x = value_x
        value_text.y = value_y + baseline_lift
        value_text.draw()

    def _restart_plaque_box(self):
        arrow_w, gap, pad_x, pad_y = 15, 18, 24, 13
        content_w = arrow_w + gap + self.restart_w + gap + arrow_w
        content_h = max(self.restart_h, 21)
        box_w = content_w + pad_x * 2
        box_h = content_h + pad_y * 2
        box_left = (TITLE_REF_WIDTH - box_w) / 2
        return box_left, RESTART_TOP, box_w, box_h

    def _is_over_restart(self, x, y):
        box_left, box_top, box_w, box_h = self._restart_plaque_box()
        rect = self.design_rect(box_left, box_top, box_w, box_h)
        return rect.left <= x <= rect.right and rect.bottom <= y <= rect.top

    def _draw_restart_plaque(self):
        arrow_w, gap, pad_x, pad_y = 15, 18, 24, 13
        border = 3
        box_left, box_top, box_w, box_h = self._restart_plaque_box()
        content_h = max(self.restart_h, 21)
        hover = self.restart_hover_scale
        center_x = box_left + box_w / 2
        center_y = box_top + box_h / 2

        def prect(left, top, w, h):
            return self.design_rect(
                center_x + (left - center_x) * hover,
                center_y + (top - center_y) * hover,
                w * hover, h * hover,
            )

        arcade.draw_rect_filled(prect(box_left - border, box_top - border, box_w + border * 2, box_h + border * 2), GO_PLAQUE_BORDER)
        arcade.draw_rect_filled(prect(box_left, box_top, box_w, box_h), GO_PLAQUE_FILL)

        for rx, ry in ((box_left - 3, box_top - 3), (box_left + box_w - 5, box_top - 3),
                       (box_left - 3, box_top + box_h - 5), (box_left + box_w - 5, box_top + box_h - 5)):
            arcade.draw_rect_filled(prect(rx, ry, 8, 8), GO_PLAQUE_BORDER)

        content_top = box_top + pad_y
        nudge = 5 if int(self.elapsed / 0.45) % 2 == 0 else 0

        self._draw_arrow(prect, box_left + pad_x + nudge, content_top, content_h, facing_right=True)
        self._draw_arrow(prect, box_left + box_w - pad_x - arrow_w - nudge, content_top, content_h, facing_right=False)

        blink_on = (self.elapsed % 1.1) < 0.55
        if blink_on:
            text_left = box_left + pad_x + arrow_w + gap
            text_top = content_top + (content_h - self.restart_h) / 2
            arcade.draw_texture_rect(self.restart_texture, prect(text_left, text_top, self.restart_w, self.restart_h), pixelated=True)

    def _draw_arrow(self, prect, x, top, content_h, facing_right):
        mid = top + (content_h - 21) / 2
        if facing_right:
            arcade.draw_rect_filled(prect(x, mid, 5, 21), GO_PLAQUE_BORDER)
            arcade.draw_rect_filled(prect(x + 5, mid + 4, 5, 13), GO_PLAQUE_BORDER)
            arcade.draw_rect_filled(prect(x + 10, mid + 8, 5, 5), GO_PLAQUE_BORDER)
        else:
            arcade.draw_rect_filled(prect(x + 10, mid, 5, 21), GO_PLAQUE_BORDER)
            arcade.draw_rect_filled(prect(x + 5, mid + 4, 5, 13), GO_PLAQUE_BORDER)
            arcade.draw_rect_filled(prect(x, mid + 8, 5, 5), GO_PLAQUE_BORDER)

    def _draw_crt(self):
        arcade.draw_texture_rect(self.crt_texture, self.design_rect(0, 0, TITLE_REF_WIDTH, TITLE_REF_HEIGHT), pixelated=True)

    # input / lifecycle 

    def on_key_press(self, key):
        pass

    def on_key_release(self, key):
        pass

    def on_mouse_motion(self, x, y):
        self.mouse_x, self.mouse_y = x, y
        was_hovering = self.is_hovering_restart
        self.is_hovering_restart = self._is_over_restart(x, y)
        if self.is_hovering_restart and not was_hovering and self.audio:
            self.audio.play_hover()

    def on_mouse_press(self, x, y):
        if self._is_over_restart(x, y):
            self.on_back()

    def on_mouse_release(self):
        pass

    def on_resize(self, width, height):
        self.screen.resize(width, height)
        self.camera.match_window(position=True)
