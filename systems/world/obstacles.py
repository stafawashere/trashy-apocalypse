import arcade
from constants import SOLID_RECTS, MAP_PIXEL_HEIGHT

MAX_RESOLVE_PASSES = 16
SEPARATION_EPSILON = 0.5


class Obstacles:
    def __init__(self, local_player, sprite_list=None):
        self.local_player = local_player
        self.sprite_list = arcade.SpriteList(use_spatial_hash=True)

        for left, top, width, height in SOLID_RECTS:
            center_x = left + width / 2
            center_y = MAP_PIXEL_HEIGHT - (top + height / 2)
            solid = arcade.SpriteSolidColor(width, height, color=arcade.color.RED)
            solid.center_x = center_x
            solid.center_y = center_y
            self.sprite_list.append(solid)

        if sprite_list is not None:
            sprite_list.extend(self.sprite_list)

    def update(self):
        self.resolve(self.local_player.sprite)

    def resolve(self, sprite):
        for _ in range(MAX_RESOLVE_PASSES):
            hits = arcade.check_for_collision_with_list(sprite, self.sprite_list)
            if not hits:
                break

            push_x = 0.0
            push_y = 0.0
            for obstacle in hits:
                axis_push_x, axis_push_y = self.separation(sprite, obstacle)
                if abs(axis_push_x) > abs(push_x):
                    push_x = axis_push_x
                if abs(axis_push_y) > abs(push_y):
                    push_y = axis_push_y

            if push_x == 0 and push_y == 0:
                break

            sprite.center_x += push_x
            sprite.center_y += push_y

    def separation(self, sprite, obstacle):
        overlap_x, overlap_y = self.overlap(sprite, obstacle)
        if overlap_x <= 0 or overlap_y <= 0:
            return 0.0, 0.0

        is_shallower_on_x = overlap_x < overlap_y
        if is_shallower_on_x:
            is_sprite_left_of_obstacle = sprite.center_x < obstacle.center_x
            push = overlap_x + SEPARATION_EPSILON
            return (-push if is_sprite_left_of_obstacle else push), 0.0

        is_sprite_below_obstacle = sprite.center_y < obstacle.center_y
        push = overlap_y + SEPARATION_EPSILON
        return 0.0, (-push if is_sprite_below_obstacle else push)

    def would_collide(self, sprite, offset_x, offset_y):
        sprite.center_x += offset_x
        sprite.center_y += offset_y
        is_blocked = len(arcade.check_for_collision_with_list(sprite, self.sprite_list)) > 0
        sprite.center_x -= offset_x
        sprite.center_y -= offset_y
        return is_blocked

    def overlap(self, sprite, obstacle):
        distance_x = abs(sprite.center_x - obstacle.center_x)
        distance_y = abs(sprite.center_y - obstacle.center_y)
        overlap_x = (sprite.width + obstacle.width) / 2 - distance_x
        overlap_y = (sprite.height + obstacle.height) / 2 - distance_y
        return overlap_x, overlap_y
