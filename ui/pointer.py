import arcade
from constants import (
    POINTER_TEXTURE,
    POINTER_HEIGHT,
    POINTER_HOTSPOT_X,
    POINTER_HOTSPOT_Y,
)


class Pointer:
    def __init__(self, screen):
        self.screen = screen
        self.texture = arcade.load_texture(POINTER_TEXTURE)
        self.sprite = arcade.Sprite(self.texture)
        self.mouse_x = 0
        self.mouse_y = 0

    def on_mouse_motion(self, x, y):
        self.mouse_x = x
        self.mouse_y = y

    def draw(self):
        self.sprite.scale = POINTER_HEIGHT * self.screen.scale / self.texture.height
        self.sprite.center_x = self.mouse_x - (POINTER_HOTSPOT_X - 0.5) * self.sprite.width
        self.sprite.center_y = self.mouse_y + (POINTER_HOTSPOT_Y - 0.5) * self.sprite.height
        arcade.draw_sprite(self.sprite)
