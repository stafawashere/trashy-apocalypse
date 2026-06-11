import arcade
from constants import (
    HUD_FRAME_COUNT,
    HUD_FRAME_THRESHOLDS,
    AMMO_ICON_DIR,
    HEALTH_ICON_DIR,
    HUD_FONT_PATH,
    HUD_FONT_NAME,
    EDGE_MARGIN,
    GROUP_GAP,
    LABEL_FONT_SIZE,
    LABEL_GAP,
    AMMO_ICON_HEIGHT,
    AMMO_BAR_WIDTH,
    AMMO_BAR_HEIGHT,
    AMMO_BAR_BASELINE_NUDGE,
    HEALTH_ICON_HEIGHT,
    HEALTH_ICON_GAP,
    HEALTH_BAR_WIDTH,
    HEALTH_BAR_HEIGHT,
    TANK_TRACK_COLOR,
    TANK_BORDER_COLOR,
    TANK_FILL_COLOR,
    TANK_LABEL_COLOR,
    HEALTH_TRACK_COLOR,
    HEALTH_BORDER_COLOR,
    HEALTH_FILL_COLOR,
    HEALTH_LABEL_COLOR,
    VALUE_COLOR,
)


def frame_for_value(value):
    for frame_index, threshold in enumerate(HUD_FRAME_THRESHOLDS):
        if value > threshold:
            return frame_index
    return HUD_FRAME_COUNT - 1


def bottom_padding(texture):
    bounds = texture.image.getbbox()
    bottom_y = bounds[3]
    return (texture.height - bottom_y) / texture.height


def left_padding(texture):
    bounds = texture.image.getbbox()
    return bounds[0] / texture.width


class Hud:
    def __init__(self, blaster, local_player, screen):
        self.blaster = blaster
        self.local_player = local_player
        self.screen = screen
        self.camera = arcade.Camera2D()

        arcade.load_font(HUD_FONT_PATH)

        self.ammo_frames = [arcade.load_texture(f"{AMMO_ICON_DIR}/ui_windex_{i}.png") for i in range(HUD_FRAME_COUNT)]
        self.ammo_icon = arcade.Sprite(self.ammo_frames[0])
        self.ammo_bottom_padding = bottom_padding(self.ammo_icon.texture)
        self.ammo_label = arcade.Text("SOLUTION", 0, 0, TANK_LABEL_COLOR, LABEL_FONT_SIZE, font_name=HUD_FONT_NAME, anchor_x="left", anchor_y="bottom")
        self.ammo_value = arcade.Text("100/100", 0, 0, VALUE_COLOR, LABEL_FONT_SIZE, font_name=HUD_FONT_NAME, anchor_x="right", anchor_y="bottom")

        self.health_frames = [arcade.load_texture(f"{HEALTH_ICON_DIR}/ui_health_{i}.png") for i in range(HUD_FRAME_COUNT)]
        self.health_icon = arcade.Sprite(self.health_frames[0])
        self.health_left_padding = left_padding(self.health_icon.texture)
        self.health_label = arcade.Text("HEALTH", 0, 0, HEALTH_LABEL_COLOR, LABEL_FONT_SIZE, font_name=HUD_FONT_NAME, anchor_x="left", anchor_y="top")
        self.health_value = arcade.Text("100/100", 0, 0, VALUE_COLOR, LABEL_FONT_SIZE, font_name=HUD_FONT_NAME, anchor_x="right", anchor_y="top")

        self.layout()

    @property
    def ui_scale(self):
        return self.screen.scale

    def anchor(self, fraction_x, fraction_y, nudge_x=0, nudge_y=0):
        return (
            fraction_x * self.screen.width + nudge_x * self.ui_scale,
            fraction_y * self.screen.height + nudge_y * self.ui_scale,
        )

    def layout(self):
        self.layout_ammo()
        self.layout_health()

    def layout_ammo(self):
        scale = self.ui_scale
        icon_height = AMMO_ICON_HEIGHT * scale
        icon_width = icon_height * self.ammo_icon.texture.width / self.ammo_icon.texture.height

        right_edge, bottom_edge = self.anchor(1, 0, -EDGE_MARGIN, EDGE_MARGIN)

        self.ammo_bar_right = right_edge - icon_width - GROUP_GAP * scale
        self.ammo_bar_left = self.ammo_bar_right - AMMO_BAR_WIDTH * scale
        self.ammo_bar_bottom = bottom_edge + AMMO_BAR_BASELINE_NUDGE * scale

        visible_bottom_offset = self.ammo_bottom_padding * icon_height
        self.ammo_icon.scale = icon_height / self.ammo_icon.texture.height
        self.ammo_icon.center_x = right_edge - icon_width / 2
        self.ammo_icon.center_y = self.ammo_bar_bottom + icon_height / 2 - visible_bottom_offset

        label_baseline = self.ammo_bar_bottom + AMMO_BAR_HEIGHT * scale + LABEL_GAP * scale
        self.ammo_label.x, self.ammo_label.y = self.ammo_bar_left, label_baseline
        self.ammo_value.x, self.ammo_value.y = self.ammo_bar_right, label_baseline
        self.ammo_label.font_size = self.ammo_value.font_size = LABEL_FONT_SIZE * scale

    def layout_health(self):
        scale = self.ui_scale
        font_size = LABEL_FONT_SIZE * scale
        icon_height = HEALTH_ICON_HEIGHT * scale
        icon_width = icon_height * self.health_icon.texture.width / self.health_icon.texture.height

        left_edge, top_edge = self.anchor(0, 1, EDGE_MARGIN, -EDGE_MARGIN)

        self.health_label.font_size = font_size
        self.health_value.font_size = font_size

        label_top = top_edge
        text_height = self.health_label.content_height
        text_row_width = self.health_label.content_width + self.health_value.content_width
        bar_width = max(HEALTH_BAR_WIDTH * scale, text_row_width)

        self.health_bar_left = left_edge + icon_width + HEALTH_ICON_GAP * scale
        self.health_bar_right = self.health_bar_left + bar_width
        self.health_bar_top = label_top - text_height - LABEL_GAP * scale
        self.health_bar_bottom = self.health_bar_top - HEALTH_BAR_HEIGHT * scale

        self.health_label.x, self.health_label.y = self.health_bar_left, label_top
        self.health_value.x, self.health_value.y = self.health_bar_right, label_top

        group_center_y = (label_top + self.health_bar_bottom) / 2
        self.health_icon.scale = icon_height / self.health_icon.texture.height
        self.health_icon.center_x = left_edge + icon_width / 2 - self.health_left_padding * icon_width
        self.health_icon.center_y = group_center_y

    def on_resize(self):
        self.camera.match_window(position=True)
        self.layout()

    def use(self):
        self.camera.use()

    def draw(self):
        self.draw_ammo()
        self.draw_health()

    def draw_ammo(self):
        scale = self.ui_scale
        bar_width = AMMO_BAR_WIDTH * scale
        bar_height = AMMO_BAR_HEIGHT * scale
        fill_width = bar_width * self.blaster.tank_fraction

        self.ammo_icon.texture = self.ammo_frames[frame_for_value(self.blaster.tank)]
        arcade.draw_sprite(self.ammo_icon)

        arcade.draw_lbwh_rectangle_filled(self.ammo_bar_left, self.ammo_bar_bottom, bar_width, bar_height, TANK_TRACK_COLOR)
        arcade.draw_lbwh_rectangle_filled(self.ammo_bar_left, self.ammo_bar_bottom, fill_width, bar_height, TANK_FILL_COLOR)
        arcade.draw_lbwh_rectangle_outline(self.ammo_bar_left, self.ammo_bar_bottom, bar_width, bar_height, TANK_BORDER_COLOR, 2 * scale)

        self.ammo_value.text = f"{int(round(self.blaster.tank))}/100"
        self.ammo_label.draw()
        self.ammo_value.draw()

    def draw_health(self):
        scale = self.ui_scale
        bar_width = self.health_bar_right - self.health_bar_left
        bar_height = HEALTH_BAR_HEIGHT * scale
        health = self.local_player.health
        fill_width = bar_width * health / 100

        self.health_icon.texture = self.health_frames[frame_for_value(health)]
        arcade.draw_sprite(self.health_icon)

        arcade.draw_lbwh_rectangle_filled(self.health_bar_left, self.health_bar_bottom, bar_width, bar_height, HEALTH_TRACK_COLOR)
        arcade.draw_lbwh_rectangle_filled(self.health_bar_left, self.health_bar_bottom, fill_width, bar_height, HEALTH_FILL_COLOR)
        arcade.draw_lbwh_rectangle_outline(self.health_bar_left, self.health_bar_bottom, bar_width, bar_height, HEALTH_BORDER_COLOR, 2 * scale)

        self.health_value.text = f"{int(round(health))}/100"
        self.health_label.draw()
        self.health_value.draw()
