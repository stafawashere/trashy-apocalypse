import math

import arcade

from constants import (
    PLAQUE_FILL,
    PLAQUE_BORDER,
    PLAQUE_INNER,
    PLAQUE_TEXT,
    CREDIT_LABEL_COLOR,
    CREDIT_NAME_COLOR,
    TITLE_REF_WIDTH,
    TITLE_REF_HEIGHT,
    BADGE_BOTTOM,
    BADGE_LEFT,
    BADGE_DISPLAY,
    PLAQUE_TOP,
    CREDIT_FONT_PATH,
    CREDIT_FONT_NAME,
)
from scenes.apocalypse import ApocalypseScene, baked_assets, baked_text


class TitleScene(ApocalypseScene):
    def __init__(self, screen, on_start):
        super().__init__(screen, show_logo=True)
        self.on_start = on_start
        self.started = False

        self.badge_texture = baked_assets()["badge"]
        self.press_start_texture, self.press_start_w, self.press_start_h = baked_text(
            "PRESS START", 2, PLAQUE_TEXT, PLAQUE_INNER
        )
        self.credit_name_texture, self.credit_name_w, self.credit_name_h = baked_text(
            "ARTS AND TECHNOLOGY", 2, CREDIT_NAME_COLOR, (0, 0, 0)
        )

        arcade.load_font(CREDIT_FONT_PATH)
        self.credit_label = arcade.Text(
            "PRODUCED BY", 0, 0, CREDIT_LABEL_COLOR, 19,
            font_name=CREDIT_FONT_NAME, anchor_x="left", anchor_y="center",
        )

        self.is_hovering_start = False
        self.start_hover_scale = 1.0

    # plaque geometry (design space): left, top, width, height of the PRESS START box
    def _plaque_box(self):
        arrow_w, gap, pad_x, pad_y = 15, 18, 24, 13
        content_w = arrow_w + gap + self.press_start_w + gap + arrow_w
        content_h = max(self.press_start_h, 21)
        box_w = content_w + pad_x * 2
        box_h = content_h + pad_y * 2
        box_left = (TITLE_REF_WIDTH - box_w) / 2
        return box_left, PLAQUE_TOP, box_w, box_h

    def _is_over_start(self, x, y):
        box_left, box_top, box_w, box_h = self._plaque_box()
        rect = self.design_rect(box_left, box_top, box_w, box_h)
        return rect.left <= x <= rect.right and rect.bottom <= y <= rect.top

    #update

    def update(self, delta_time):
        dt = self.advance_backdrop(delta_time)
        target_scale = 1.07 if self.is_hovering_start else 1.0
        self.start_hover_scale += (target_scale - self.start_hover_scale) * min(1.0, dt * 14)

    #draw

    def draw(self):
        self.camera.use()
        self.draw_backdrop()
        self.draw_logo()
        self.draw_crt()
        self._draw_plaque()
        self._draw_credit()

    def _draw_plaque(self):
        arrow_w, gap, pad_x, pad_y = 15, 18, 24, 13
        border = 3
        box_left, box_top, box_w, box_h = self._plaque_box()
        content_h = max(self.press_start_h, 21)
        text_w, text_h = self.press_start_w, self.press_start_h

        center_x = box_left + box_w / 2
        center_y = box_top + box_h / 2
        hover = self.start_hover_scale

        def prect(left, top, w, h):
            return self.design_rect(
                center_x + (left - center_x) * hover,
                center_y + (top - center_y) * hover,
                w * hover, h * hover,
            )

        arcade.draw_rect_filled(prect(box_left - border, box_top - border, box_w + border * 2, box_h + border * 2), PLAQUE_BORDER)
        arcade.draw_rect_filled(prect(box_left, box_top, box_w, box_h), PLAQUE_FILL)

        for rx, ry in ((box_left - 3, box_top - 3), (box_left + box_w - 5, box_top - 3),
                       (box_left - 3, box_top + box_h - 5), (box_left + box_w - 5, box_top + box_h - 5)):
            arcade.draw_rect_filled(prect(rx, ry, 8, 8), PLAQUE_BORDER)

        content_top = box_top + pad_y
        nudge = 5 if int(self.elapsed / 0.45) % 2 == 0 else 0

        self._draw_arrow(prect, box_left + pad_x + nudge, content_top, content_h, facing_right=True)
        self._draw_arrow(prect, box_left + box_w - pad_x - arrow_w - nudge, content_top, content_h, facing_right=False)

        blink_on = (self.elapsed % 1.1) < 0.495
        if blink_on or self.started:
            text_left = box_left + pad_x + arrow_w + gap
            text_top = content_top + (content_h - text_h) / 2
            arcade.draw_texture_rect(self.press_start_texture, prect(text_left, text_top, text_w, text_h), pixelated=True)

    def _draw_arrow(self, prect, x, top, content_h, facing_right):
        mid = top + (content_h - 21) / 2
        if facing_right:
            arcade.draw_rect_filled(prect(x, mid, 5, 21), PLAQUE_BORDER)
            arcade.draw_rect_filled(prect(x + 5, mid + 4, 5, 13), PLAQUE_BORDER)
            arcade.draw_rect_filled(prect(x + 10, mid + 8, 5, 5), PLAQUE_BORDER)
        else:
            arcade.draw_rect_filled(prect(x + 10, mid, 5, 21), PLAQUE_BORDER)
            arcade.draw_rect_filled(prect(x + 5, mid + 4, 5, 13), PLAQUE_BORDER)
            arcade.draw_rect_filled(prect(x, mid + 8, 5, 5), PLAQUE_BORDER)

    def _draw_credit(self):
        scale = self.comp_scale
        bob = -2 * (1 - math.cos(self.elapsed / 3.4 * 2 * math.pi))
        badge_top = (TITLE_REF_HEIGHT - BADGE_BOTTOM - BADGE_DISPLAY) + bob
        arcade.draw_texture_rect(self.badge_texture, self.design_rect(BADGE_LEFT, badge_top, BADGE_DISPLAY, BADGE_DISPLAY), pixelated=True)

        text_left = BADGE_LEFT + BADGE_DISPLAY + 14
        badge_center = badge_top + BADGE_DISPLAY / 2

        label_h, gap, name_h = 15, 6, 16
        name_w = self.credit_name_w * (name_h / self.credit_name_h)
        block_h = label_h + gap + name_h
        block_top = badge_center - block_h / 2

        self.credit_label.font_size = 19 * scale
        self.credit_label.x = self.comp_left + text_left * scale
        self.credit_label.y = self.comp_bottom + (TITLE_REF_HEIGHT - (block_top + label_h / 2)) * scale
        self.credit_label.draw()

        arcade.draw_texture_rect(
            self.credit_name_texture,
            self.design_rect(text_left, block_top + label_h + gap, name_w, name_h),
            pixelated=True,
        )

    #input / lifecycle

    def _start(self):
        if self.started:
            return
        self.started = True
        self.on_start()

    def on_key_press(self, key):
        self._start()

    def on_key_release(self, key):
        pass

    def on_mouse_motion(self, x, y):
        self.mouse_x, self.mouse_y = x, y
        self.is_hovering_start = self._is_over_start(x, y)

    def on_mouse_press(self, x, y):
        if self._is_over_start(x, y):
            self._start()

    def on_mouse_release(self):
        pass
