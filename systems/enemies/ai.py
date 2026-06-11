import math
from constants import ZOMBIE_SPEED

LOOKAHEAD_DISTANCE = 18
STEER_ANGLES = [0, math.radians(45), math.radians(-45), math.radians(90), math.radians(-90)]


class ZombieChase:
    def __init__(self, local_player, spawner, obstacles=None, speed=ZOMBIE_SPEED):
        self.local_player = local_player
        self.spawner = spawner
        self.obstacles = obstacles
        self.speed = speed

    def update(self):
        target_x = self.local_player.sprite.center_x
        target_y = self.local_player.sprite.center_y
        for zombie in self.spawner.zombies:
            self.step_toward(zombie.sprite, target_x, target_y)

    def step_toward(self, zombie_sprite, target_x, target_y):
        toward_x = target_x - zombie_sprite.center_x
        toward_y = target_y - zombie_sprite.center_y
        distance = math.hypot(toward_x, toward_y)
        if distance == 0:
            zombie_sprite.change_x = 0
            zombie_sprite.change_y = 0
            return

        desired_heading = math.atan2(toward_y, toward_x)
        heading = self.unblocked_heading(zombie_sprite, desired_heading)

        zombie_sprite.change_x = math.cos(heading) * self.speed
        zombie_sprite.change_y = math.sin(heading) * self.speed

    def unblocked_heading(self, zombie_sprite, desired_heading):
        if self.obstacles is None:
            return desired_heading

        for angle_offset in STEER_ANGLES:
            heading = desired_heading + angle_offset
            offset_x = math.cos(heading) * LOOKAHEAD_DISTANCE
            offset_y = math.sin(heading) * LOOKAHEAD_DISTANCE
            if not self.obstacles.would_collide(zombie_sprite, offset_x, offset_y):
                return heading

        return desired_heading
