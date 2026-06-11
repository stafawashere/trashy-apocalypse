import math
import arcade
from constants import (
    BULLET_TEXTURE,
    PUFF_TEXTURE,
    PUFF_SCALE,
    BULLET_FADE_MULTIPLIER,
    PUFF_LIFESPAN,
    PUFF_GROWTH,
    PUFF_PEAK_ALPHA,
)


class SprayBullet:
    def __init__(self, origin_x, origin_y, direction_radians, speed, lifespan, scale, sprite_list):
        self.velocity_x = math.cos(direction_radians) * speed
        self.velocity_y = math.sin(direction_radians) * speed
        self.lifespan = lifespan
        self.seconds_alive = 0.0

        self.sprite = arcade.Sprite(BULLET_TEXTURE, scale=scale)
        self.sprite.center_x = origin_x
        self.sprite.center_y = origin_y
        self.sprite.angle = -math.degrees(direction_radians)
        sprite_list.append(self.sprite)

    @property
    def is_expired(self):
        return self.seconds_alive >= self.lifespan

    def advance(self, delta_time):
        self.sprite.center_x += self.velocity_x * delta_time
        self.sprite.center_y += self.velocity_y * delta_time
        self.seconds_alive += delta_time
        self.sprite.alpha = self.fade_alpha()

    def fade_alpha(self):
        remaining_fraction = 1.0 - self.seconds_alive / self.lifespan
        return max(0, min(255, int(remaining_fraction * BULLET_FADE_MULTIPLIER * 255)))

    def destroy(self):
        self.sprite.remove_from_sprite_lists()


class SprayPuff:
    def __init__(self, x, y, direction_radians, sprite_list):
        self.lifespan = PUFF_LIFESPAN
        self.seconds_alive = 0.0
        self.base_scale = PUFF_SCALE

        self.sprite = arcade.Sprite(PUFF_TEXTURE, scale=PUFF_SCALE)
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.sprite.angle = -math.degrees(direction_radians)
        sprite_list.append(self.sprite)

    @property
    def is_expired(self):
        return self.seconds_alive >= self.lifespan

    def advance(self, delta_time):
        self.seconds_alive += delta_time
        life_fraction = self.seconds_alive / self.lifespan
        self.sprite.scale = self.base_scale * (1.0 + PUFF_GROWTH * life_fraction)
        self.sprite.alpha = max(0, int((1.0 - life_fraction) * PUFF_PEAK_ALPHA * 255))

    def destroy(self):
        self.sprite.remove_from_sprite_lists()
