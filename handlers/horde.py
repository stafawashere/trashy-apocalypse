import math
import random

from objects.__init__ import Zombie


class Horde:
    def __init__(self, player, map, player_speed=4, spawn_interval=10, sprite_list=None):
        self.player = player
        self.map = map
        self.walk_speed = player_speed * 0.7
        self.spawn_interval = spawn_interval
        self.sprite_list = sprite_list
        self.zombies = []
        self.time_since_spawn = 0

    def spawn(self):
        spawn_x = random.uniform(0, self.map.width)
        spawn_y = random.uniform(0, self.map.height)
        zombie = Zombie(x=spawn_x, y=spawn_y, sprite_list=self.sprite_list)
        self.zombies.append(zombie)

    def update(self, delta_time):
        self.time_since_spawn += delta_time
        if self.time_since_spawn >= self.spawn_interval:
            self.spawn()
            self.time_since_spawn = 0

        for zombie in self.zombies:
            gap_to_player_x = self.player.sprite.center_x - zombie.sprite.center_x
            gap_to_player_y = self.player.sprite.center_y - zombie.sprite.center_y
            zombie.sprite.angle = math.degrees(math.atan2(gap_to_player_y, -gap_to_player_x))

            distance_to_player = math.hypot(gap_to_player_x, gap_to_player_y)
            if distance_to_player > 0:
                zombie.sprite.center_x += gap_to_player_x / distance_to_player * self.walk_speed
                zombie.sprite.center_y += gap_to_player_y / distance_to_player * self.walk_speed

        self.push_overlapping_zombies_apart()
        self.keep_zombies_off_player()

    def push_overlapping_zombies_apart(self):
        for zombie_index, zombie in enumerate(self.zombies):
            for other_zombie in self.zombies[zombie_index + 1:]:
                gap_x = other_zombie.sprite.center_x - zombie.sprite.center_x
                gap_y = other_zombie.sprite.center_y - zombie.sprite.center_y
                distance_between_zombies = math.hypot(gap_x, gap_y)
                min_distance_apart = (zombie.sprite.width + other_zombie.sprite.width) / 2

                if distance_between_zombies == 0:
                    gap_x = zombie_index + 1
                    distance_between_zombies = zombie_index + 1

                if distance_between_zombies < min_distance_apart:
                    overlap_amount = min_distance_apart - distance_between_zombies
                    push_x = gap_x / distance_between_zombies * overlap_amount / 2
                    push_y = gap_y / distance_between_zombies * overlap_amount / 2

                    zombie.sprite.center_x -= push_x
                    zombie.sprite.center_y -= push_y
                    other_zombie.sprite.center_x += push_x
                    other_zombie.sprite.center_y += push_y

    def keep_zombies_off_player(self):
        for zombie_index, zombie in enumerate(self.zombies):
            gap_from_player_x = zombie.sprite.center_x - self.player.sprite.center_x
            gap_from_player_y = zombie.sprite.center_y - self.player.sprite.center_y
            distance_to_player = math.hypot(gap_from_player_x, gap_from_player_y)
            min_distance_to_player = (zombie.sprite.width + self.player.sprite.width) / 2

            if distance_to_player == 0:
                gap_from_player_x = zombie_index + 1
                distance_to_player = zombie_index + 1

            if distance_to_player < min_distance_to_player:
                zombie.sprite.center_x = self.player.sprite.center_x + gap_from_player_x / distance_to_player * min_distance_to_player
                zombie.sprite.center_y = self.player.sprite.center_y + gap_from_player_y / distance_to_player * min_distance_to_player
