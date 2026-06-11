import arcade
from constants import FRAME_SIZE, ANIMATION_FRAME_COUNT, FACING_DOWN, FACING_UP, FACING_LEFT, FACING_RIGHT


def load_animation_frames(sheet_name, asset_dir):
    sheet = arcade.load_spritesheet(f"{asset_dir}/{sheet_name}.png")
    return sheet.get_texture_grid(
        size=(FRAME_SIZE, FRAME_SIZE),
        columns=ANIMATION_FRAME_COUNT,
        count=ANIMATION_FRAME_COUNT,
    )


def directional_frames(side_sheet_name, up_sheet_name, down_sheet_name, asset_dir):
    right_frames = load_animation_frames(side_sheet_name, asset_dir)
    return {
        FACING_DOWN: load_animation_frames(down_sheet_name, asset_dir),
        FACING_UP: load_animation_frames(up_sheet_name, asset_dir),
        FACING_RIGHT: right_frames,
        FACING_LEFT: [frame.flip_left_right() for frame in right_frames],
    }


def facing_for_velocity(velocity_x, velocity_y):
    priority_is_horizontal = abs(velocity_x) > abs(velocity_y)
    if priority_is_horizontal:
        return FACING_RIGHT if velocity_x > 0 else FACING_LEFT
    return FACING_UP if velocity_y > 0 else FACING_DOWN
