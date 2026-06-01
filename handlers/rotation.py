import math


class Rotation:
    def __init__(self, player, camera, angle_offset=0):
        self.player = player
        self.camera = camera
        self.angle_offset = angle_offset
        self.mouse_x = player.sprite.center_x
        self.mouse_y = player.sprite.center_y

    def on_mouse_motion(self, x, y):
        self.mouse_x = x
        self.mouse_y = y

        self.update_player_angle()

    def update_player_angle(self):
        mouse_in_world = self.camera.camera.unproject((self.mouse_x, self.mouse_y))
        aim_x = mouse_in_world.x - self.player.sprite.center_x
        aim_y = mouse_in_world.y - self.player.sprite.center_y
        angle = math.degrees(math.atan2(aim_y, -aim_x))

        self.player.sprite.angle = angle + self.angle_offset
        return angle

    def update(self):
        self.update_player_angle()
