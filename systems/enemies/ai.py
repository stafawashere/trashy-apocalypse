import math
from constants import ZOMBIE_SPEED


class ZombieChase:
    def __init__(self, local_player, spawner, speed=ZOMBIE_SPEED):
        self.local_player = local_player
        self.spawner = spawner
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

        zombie_sprite.change_x = toward_x / distance * self.speed
        zombie_sprite.change_y = toward_y / distance * self.speed
