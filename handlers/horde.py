import math
from constants import ZOMBIE_SPEED, COLLISION_RADIUS_FRACTION


class Horde:
    def __init__(self, local_player, spawner, speed=ZOMBIE_SPEED):
        self.local_player = local_player
        self.spawner = spawner
        self.speed = speed

    @property
    def zombies(self):
        return self.spawner.zombies

    def chase(self):
        target_x = self.local_player.sprite.center_x
        target_y = self.local_player.sprite.center_y
        for zombie in self.zombies:
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

    def collide(self):
        self.separate_zombies()
        self.push_off_player()

    def separate_zombies(self):
        zombie_sprites = [zombie.sprite for zombie in self.zombies]
        for index, zombie_sprite in enumerate(zombie_sprites):
            for other_sprite in zombie_sprites[index + 1:]:
                self.resolve_overlap(zombie_sprite, other_sprite)

    def resolve_overlap(self, a, b):
        toward_x, toward_y, distance = self.separation(a, b)
        min_distance = self.collision_radius(a) + self.collision_radius(b)
        if distance >= min_distance:
            return

        half_push = (min_distance - distance) / 2
        a.center_x -= toward_x * half_push
        a.center_y -= toward_y * half_push
        b.center_x += toward_x * half_push
        b.center_y += toward_y * half_push

    def push_off_player(self):
        player_sprite = self.local_player.sprite
        for zombie in self.zombies:
            toward_x, toward_y, distance = self.separation(player_sprite, zombie.sprite)
            min_distance = self.collision_radius(player_sprite) + self.collision_radius(zombie.sprite)
            if distance >= min_distance:
                continue

            zombie.sprite.center_x = player_sprite.center_x + toward_x * min_distance
            zombie.sprite.center_y = player_sprite.center_y + toward_y * min_distance

    def separation(self, origin, other):
        offset_x = other.center_x - origin.center_x
        offset_y = other.center_y - origin.center_y
        distance = math.hypot(offset_x, offset_y)
        if distance == 0:
            return 1.0, 0.0, 0.0
            
        return offset_x / distance, offset_y / distance, distance

    def collision_radius(self, sprite):
        return sprite.width * COLLISION_RADIUS_FRACTION
