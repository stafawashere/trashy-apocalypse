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
        sprite_box = self.hitbox_bounds(sprite)
        obstacle_box = self.hitbox_bounds(obstacle)
        overlap_x, overlap_y = self.overlap(sprite_box, obstacle_box)
        if overlap_x <= 0 or overlap_y <= 0:
            return 0.0, 0.0

        sprite_center_x = (sprite_box[0] + sprite_box[1]) / 2
        sprite_center_y = (sprite_box[2] + sprite_box[3]) / 2
        obstacle_center_x = (obstacle_box[0] + obstacle_box[1]) / 2
        obstacle_center_y = (obstacle_box[2] + obstacle_box[3]) / 2

        is_shallower_on_x = overlap_x < overlap_y
        if is_shallower_on_x:
            is_sprite_left_of_obstacle = sprite_center_x < obstacle_center_x
            push = overlap_x + SEPARATION_EPSILON
            return (-push if is_sprite_left_of_obstacle else push), 0.0

        is_sprite_below_obstacle = sprite_center_y < obstacle_center_y
        push = overlap_y + SEPARATION_EPSILON
        return 0.0, (-push if is_sprite_below_obstacle else push)

    def would_collide(self, sprite, offset_x, offset_y):
        sprite.center_x += offset_x
        sprite.center_y += offset_y
        is_blocked = len(arcade.check_for_collision_with_list(sprite, self.sprite_list)) > 0
        sprite.center_x -= offset_x
        sprite.center_y -= offset_y
        return is_blocked

    def hitbox_bounds(self, sprite):
        points = sprite.hit_box.get_adjusted_points()
        xs = [point[0] for point in points]
        ys = [point[1] for point in points]
        return min(xs), max(xs), min(ys), max(ys)

    def overlap(self, sprite_box, obstacle_box):
        overlap_x = min(sprite_box[1], obstacle_box[1]) - max(sprite_box[0], obstacle_box[0])
        overlap_y = min(sprite_box[3], obstacle_box[3]) - max(sprite_box[2], obstacle_box[2])
        return overlap_x, overlap_y
