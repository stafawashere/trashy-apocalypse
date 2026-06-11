import arcade

LOCAL_PLAYER_ASSET_DIR = "assets/local_player"
PLAYER_SPRITE_SCALE = 0.1
FRAME_SIZE = 432
FRAME_COUNT = 4
SECONDS_PER_FRAME = 0.1
MAX_HEALTH = 100

FACING_DOWN = "down"
FACING_UP = "up"
FACING_LEFT = "left"
FACING_RIGHT = "right"

HAND_ANCHOR_FRACTION = {
    FACING_DOWN: (0.49, 0.69),
    FACING_UP: (0.49, 0.35),
    FACING_LEFT: (0.25, 0.56),
    FACING_RIGHT: (0.75, 0.56),
}

WALK_BOB_OFFSETS = (0.0, 2.0, -1.0, 2.0)


def load_animation_frames(sheet_name):
    sheet = arcade.load_spritesheet(f"{LOCAL_PLAYER_ASSET_DIR}/{sheet_name}.png")
    return sheet.get_texture_grid(
        size=(FRAME_SIZE, FRAME_SIZE),
        columns=FRAME_COUNT,
        count=FRAME_COUNT,
    )


def directional_frames(side_sheet_name, up_sheet_name, down_sheet_name):
    right_frames = load_animation_frames(side_sheet_name)
    return {
        FACING_DOWN: load_animation_frames(down_sheet_name),
        FACING_UP: load_animation_frames(up_sheet_name),
        FACING_RIGHT: right_frames,
        FACING_LEFT: [frame.flip_left_right() for frame in right_frames],
    }


class LocalPlayer:
    def __init__(self, name="localplayer", x=0, y=0, sprite_list=None):
        self.name = name
        self.health = MAX_HEALTH

        self.idle_texture = arcade.load_texture(f"{LOCAL_PLAYER_ASSET_DIR}/player.png")
        self.walk_frames = directional_frames("walk_side", "walk_up", "walk_down")
        self.hold_frames = directional_frames("hold_side", "hold_up", "hold_down")

        self.facing = FACING_DOWN
        self.current_frame_index = 0
        self.seconds_on_current_frame = 0.0
        self.held_item = None
        self.aim_target = None

        self.sprite = arcade.Sprite(self.idle_texture, scale=PLAYER_SPRITE_SCALE)
        self.sprite.center_x = x
        self.sprite.center_y = y

        if sprite_list is not None:
            sprite_list.append(self.sprite)

    @property
    def is_holding(self):
        return self.held_item is not None

    @property
    def is_facing_away(self):
        return self.facing == FACING_UP

    def hold(self, item):
        self.held_item = item

    def aim_at(self, target):
        self.aim_target = target

    def update_animation(self, delta_time):
        velocity_x = self.sprite.change_x
        velocity_y = self.sprite.change_y
        is_standing_still = velocity_x == 0 and velocity_y == 0
        frames = self.hold_frames if self.is_holding else self.walk_frames

        if self.is_holding:
            self.face_aim_target()
        elif not is_standing_still:
            self.facing = self.facing_for_velocity(velocity_x, velocity_y)

        if is_standing_still:
            self.show_idle(frames)
        else:
            self.advance_frame(delta_time)
            self.sprite.texture = frames[self.facing][self.current_frame_index]

        self.update_held_item()

    def show_idle(self, frames):
        self.current_frame_index = 0
        self.seconds_on_current_frame = 0.0
        if self.is_holding:
            self.sprite.texture = frames[self.facing][0]
        else:
            self.sprite.texture = self.idle_texture

    def facing_for_velocity(self, velocity_x, velocity_y):
        priority_is_horizontal = abs(velocity_x) > abs(velocity_y)
        if priority_is_horizontal:
            return FACING_RIGHT if velocity_x > 0 else FACING_LEFT
        return FACING_UP if velocity_y > 0 else FACING_DOWN

    def advance_frame(self, delta_time):
        self.seconds_on_current_frame += delta_time
        if self.seconds_on_current_frame >= SECONDS_PER_FRAME:
            self.seconds_on_current_frame -= SECONDS_PER_FRAME
            self.current_frame_index = (self.current_frame_index + 1) % FRAME_COUNT

    def face_aim_target(self):
        if self.aim_target is None:
            return
        aim_x, aim_y = self.aim_target
        delta_x = aim_x - self.sprite.center_x
        delta_y = aim_y - self.sprite.center_y
        aim_is_horizontal = abs(delta_x) >= abs(delta_y)
        if aim_is_horizontal:
            self.facing = FACING_RIGHT if delta_x >= 0 else FACING_LEFT
        else:
            self.facing = FACING_UP if delta_y >= 0 else FACING_DOWN

    def update_held_item(self):
        if self.held_item is None:
            return
        pivot_x, pivot_y = self.hand_anchor()
        target_x, target_y = self.aim_target or (self.sprite.center_x, self.sprite.center_y - 100)
        self.held_item.aim_from(pivot_x, pivot_y, target_x, target_y)

    def hand_anchor(self):
        fraction_x, fraction_y = HAND_ANCHOR_FRACTION[self.facing]
        offset_x = (fraction_x - 0.5) * self.sprite.width
        offset_y = (0.5 - fraction_y) * self.sprite.height + self.walk_bob_offset(scale=0.5)
        return self.sprite.center_x + offset_x, self.sprite.center_y + offset_y

    def walk_bob_offset(self, scale=1):
        is_moving = self.sprite.change_x != 0 or self.sprite.change_y != 0
        if not is_moving:
            return 0.0
        return WALK_BOB_OFFSETS[self.current_frame_index] * scale

    def take_damage(self, amount):
        self.health = max(self.health - amount, 0)
        return self.health

    def heal(self, amount):
        self.health = min(self.health + amount, MAX_HEALTH)
        return self.health
