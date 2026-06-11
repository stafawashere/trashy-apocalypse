import random
from entities import Zombie
from constants import SPAWN_INTERVAL_SECONDS, MAX_ZOMBIES

MAX_SPAWN_ATTEMPTS = 20


class ZombieSpawner:
    def __init__(self, map, zombie_list, obstacles=None, interval_seconds=SPAWN_INTERVAL_SECONDS):
        self.map = map
        self.zombie_list = zombie_list
        self.obstacles = obstacles
        self.interval_seconds = interval_seconds
        self.seconds_since_last_spawn = 0.0
        self.zombies = []

    def update(self, delta_time):
        self.seconds_since_last_spawn += delta_time
        is_spawn_due = self.seconds_since_last_spawn >= self.interval_seconds
        if not is_spawn_due:
            return

        self.seconds_since_last_spawn -= self.interval_seconds
        self.spawn()

    def spawn(self):
        if len(self.zombies) >= MAX_ZOMBIES:
            return

        zombie = Zombie(sprite_list=self.zombie_list)
        self.place_clear_of_walls(zombie)
        self.zombies.append(zombie)

    def place_clear_of_walls(self, zombie):
        half_width = zombie.sprite.width / 2
        half_height = zombie.sprite.height / 2

        for _ in range(MAX_SPAWN_ATTEMPTS):
            zombie.sprite.center_x, zombie.sprite.center_y = self.random_point_on_map(
                half_width, half_height
            )
            if self.obstacles is None or not self.obstacles.would_collide(zombie.sprite, 0, 0):
                return

    def random_point_on_map(self, sprite_half_width, sprite_half_height):
        left = sprite_half_width
        right = self.map.width - sprite_half_width
        bottom = sprite_half_height
        top = self.map.height - sprite_half_height
        return random.uniform(left, right), random.uniform(bottom, top)
