import math
from constants import ZOMBIE_SPEED

LOOKAHEAD_DISTANCE = 18
COMMIT_RELEASE_DISTANCE = 40
DETOUR_OFFSETS = [math.radians(45), math.radians(90), math.radians(135)]


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
            self.step_toward(zombie, target_x, target_y)

    def step_toward(self, zombie, target_x, target_y):
        zombie_sprite = zombie.sprite
        toward_x = target_x - zombie_sprite.center_x
        toward_y = target_y - zombie_sprite.center_y
        distance = math.hypot(toward_x, toward_y)
        if distance == 0:
            zombie_sprite.change_x = 0
            zombie_sprite.change_y = 0
            return

        desired_heading = math.atan2(toward_y, toward_x)
        heading = self.steer(zombie, desired_heading)

        zombie_sprite.change_x = math.cos(heading) * self.speed
        zombie_sprite.change_y = math.sin(heading) * self.speed

    def steer(self, zombie, desired_heading):
        if self.obstacles is None:
            return desired_heading

        zombie_sprite = zombie.sprite
        committed_sign = getattr(zombie, "detour_sign", 0)

        is_committed = committed_sign != 0
        release_distance = COMMIT_RELEASE_DISTANCE if is_committed else LOOKAHEAD_DISTANCE
        if self.is_clear(zombie_sprite, desired_heading, release_distance):
            zombie.detour_sign = 0
            return desired_heading

        for sign in self.preferred_signs(committed_sign):
            for offset in DETOUR_OFFSETS:
                heading = desired_heading + sign * offset
                if self.is_clear(zombie_sprite, heading, LOOKAHEAD_DISTANCE):
                    zombie.detour_sign = sign
                    return heading

        return desired_heading

    def preferred_signs(self, committed_sign):
        if committed_sign > 0:
            return [1, -1]
        if committed_sign < 0:
            return [-1, 1]
        return [1, -1]

    def is_clear(self, zombie_sprite, heading, distance):
        offset_x = math.cos(heading) * distance
        offset_y = math.sin(heading) * distance
        return not self.obstacles.would_collide(zombie_sprite, offset_x, offset_y)
