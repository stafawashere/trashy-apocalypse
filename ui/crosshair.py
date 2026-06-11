import arcade
from constants import (
    CROSSHAIR_TEXTURE,
    CROSSHAIR_HEIGHT,
    CROSSHAIR_SPIN_SPEED,
    CROSSHAIR_SPIN_RESPONSE,
    CROSSHAIR_REST_SNAP,
    WINDEX_NAME,
)


class Crosshair:
    def __init__(self, local_player, blaster, screen):
        self.local_player = local_player
        self.blaster = blaster
        self.screen = screen
        self.texture = arcade.load_texture(CROSSHAIR_TEXTURE)
        self.sprite = arcade.Sprite(self.texture)
        self.mouse_x = 0
        self.mouse_y = 0
        self.angle = 0.0
        self.spin_speed = 0.0

    @property
    def is_active(self):
        player = self.local_player
        is_alive = player.health > 0
        has_windex = player.is_holding and player.held_item.name == WINDEX_NAME
        return is_alive and has_windex

    def on_mouse_motion(self, x, y):
        self.mouse_x = x
        self.mouse_y = y

    def update(self, delta_time):
        target_speed = CROSSHAIR_SPIN_SPEED if self.blaster.is_spraying else 0.0
        approach = min(1.0, CROSSHAIR_SPIN_RESPONSE * delta_time)
        self.spin_speed += (target_speed - self.spin_speed) * approach

        if self.blaster.is_spraying:
            self.angle = (self.angle + self.spin_speed * delta_time) % 360
        else:
            self.settle(delta_time)

    def settle(self, delta_time):
        self.angle = (self.angle + self.spin_speed * delta_time) % 360
        nearest_rest = round(self.angle / 90) * 90
        snap = min(1.0, CROSSHAIR_REST_SNAP * delta_time)
        self.angle += (nearest_rest - self.angle) * snap

    def draw(self):
        if not self.is_active:
            return

        self.sprite.scale = CROSSHAIR_HEIGHT * self.screen.scale / self.texture.height
        self.sprite.angle = self.angle
        self.sprite.center_x = self.mouse_x
        self.sprite.center_y = self.mouse_y
        arcade.draw_sprite(self.sprite)
