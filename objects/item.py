import arcade
from arcade.math import get_angle_degrees, rotate_point

ITEM_SCALE = 0.15

GRIP_FRACTION_X = 0.172
GRIP_FRACTION_Y = 0.484


class Item:
    def __init__(self, name, texture, x=0, y=0, scale=ITEM_SCALE, sprite_list=None):
        self.name = name
        self.sprite = arcade.Sprite(texture, scale=scale)
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.upright_texture = self.sprite.texture
        self.flipped_texture = self.upright_texture.flip_top_bottom()

        if sprite_list is not None:
            sprite_list.append(self.sprite)

    def aim_from(self, pivot_x, pivot_y, target_x, target_y):
        angle = get_angle_degrees(pivot_x, pivot_y, target_x, target_y)
        is_aiming_left = target_x < pivot_x
        self.sprite.texture = self.flipped_texture if is_aiming_left else self.upright_texture

        grip_offset_x, grip_offset_y = self.grip_offset(is_aiming_left)
        rotated_offset_x, rotated_offset_y = rotate_point(grip_offset_x, grip_offset_y, 0.0, 0.0, angle)

        self.sprite.angle = angle
        self.sprite.center_x = pivot_x - rotated_offset_x
        self.sprite.center_y = pivot_y - rotated_offset_y

    def grip_offset(self, is_aiming_left):
        offset_x = (GRIP_FRACTION_X - 0.5) * self.sprite.width
        offset_y = (0.5 - GRIP_FRACTION_Y) * self.sprite.height
        if is_aiming_left:
            offset_y = -offset_y
        return offset_x, offset_y
