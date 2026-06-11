import arcade
from constants import (
    ZOMBIE_ASSET_DIR,
    ZOMBIE_SPRITE_SCALE,
    ANIMATION_FRAME_COUNT,
    ZOMBIE_SECONDS_PER_FRAME,
    ZOMBIE_HITS_TO_DIE,
    DAMAGE_FLASH_SECONDS,
    DAMAGE_FLASH_COLOR,
    NORMAL_COLOR,
    FACING_DOWN,
)
from entities.animation import directional_frames, facing_for_velocity


class Zombie:
    def __init__(self, name="zombie", x=0, y=0, sprite_list=None):
        self.name = name

        self.idle_texture = arcade.load_texture(f"{ZOMBIE_ASSET_DIR}/zombie.png")
        self.walk_frames = directional_frames("walk_side", "walk_up", "walk_down", ZOMBIE_ASSET_DIR)

        self.facing = FACING_DOWN
        self.current_frame_index = 0
        self.seconds_on_current_frame = 0.0
        self.hits_remaining = ZOMBIE_HITS_TO_DIE
        self.flash_seconds_remaining = 0.0

        self.sprite = arcade.Sprite(self.idle_texture, scale=ZOMBIE_SPRITE_SCALE)
        self.sprite.center_x = x
        self.sprite.center_y = y

        if sprite_list is not None:
            sprite_list.append(self.sprite)

    @property
    def is_dead(self):
        return self.hits_remaining <= 0

    def take_damage(self, amount=1):
        self.hits_remaining -= amount
        self.flash_seconds_remaining = DAMAGE_FLASH_SECONDS
        return self.hits_remaining

    def update_animation(self, delta_time):
        self.update_damage_flash(delta_time)

        velocity_x = self.sprite.change_x
        velocity_y = self.sprite.change_y
        is_standing_still = velocity_x == 0 and velocity_y == 0

        if is_standing_still:
            self.current_frame_index = 0
            self.seconds_on_current_frame = 0.0
            self.sprite.texture = self.idle_texture
            return

        self.facing = facing_for_velocity(velocity_x, velocity_y)
        self.advance_frame(delta_time)
        self.sprite.texture = self.walk_frames[self.facing][self.current_frame_index]

    def advance_frame(self, delta_time):
        self.seconds_on_current_frame += delta_time
        if self.seconds_on_current_frame >= ZOMBIE_SECONDS_PER_FRAME:
            self.seconds_on_current_frame -= ZOMBIE_SECONDS_PER_FRAME
            self.current_frame_index = (self.current_frame_index + 1) % ANIMATION_FRAME_COUNT

    def update_damage_flash(self, delta_time):
        if self.flash_seconds_remaining > 0:
            self.flash_seconds_remaining -= delta_time
        is_flashing = self.flash_seconds_remaining > 0
        self.sprite.color = DAMAGE_FLASH_COLOR if is_flashing else NORMAL_COLOR
