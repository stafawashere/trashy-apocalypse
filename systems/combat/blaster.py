import math
import random
import arcade
from entities.projectile import SprayBullet, SprayPuff
from constants import (
    TANK_MAX,
    SHOT_COST,
    REFILL_PER_SECOND,
    AUTO_FIRE_INTERVAL,
    BULLET_SPEED,
    BULLET_SPEED_VARIANCE,
    BULLET_LIFESPAN,
    MAIN_SPREAD,
    DROPLET_CHANCE,
    DROPLET_SPREAD,
    DROPLET_SPEED_FACTOR,
    DROPLET_LIFESPAN,
    BULLET_DAMAGE,
    BULLET_SCALE,
    DROPLET_SCALE,
)


class Blaster:
    def __init__(self, local_player, bullet_list, puff_list, enemies=None, audio=None, obstacles=None):
        self.local_player = local_player
        self.audio = audio
        self.bullet_list = bullet_list
        self.puff_list = puff_list
        self.enemies = enemies
        self.obstacles = obstacles
        self.tank = TANK_MAX
        self.is_firing = False
        self.seconds_since_fire = AUTO_FIRE_INTERVAL
        self.seconds_since_shot = float("inf")
        self.kills = 0
        self.bullets = []
        self.puffs = []

    @property
    def tank_fraction(self):
        return self.tank / TANK_MAX

    @property
    def can_fire(self):
        has_charge = self.tank >= SHOT_COST
        return self.local_player.is_holding and has_charge

    def on_mouse_press(self):
        self.is_firing = True
        self.seconds_since_fire = AUTO_FIRE_INTERVAL

    def on_mouse_release(self):
        self.is_firing = False

    @property
    def is_spraying(self):
        spans_auto_fire_gap = AUTO_FIRE_INTERVAL * 2
        return self.is_firing and self.seconds_since_shot <= spans_auto_fire_gap

    def update(self, delta_time):
        self.seconds_since_shot += delta_time
        self.refill(delta_time)
        self.auto_fire(delta_time)
        self.advance_projectiles(delta_time)
        self.cleanup_obstacle_hits()
        self.cleanup_hits()

    def refill(self, delta_time):
        self.tank = min(TANK_MAX, self.tank + REFILL_PER_SECOND * delta_time)

    def auto_fire(self, delta_time):
        if not self.is_firing:
            return

        self.seconds_since_fire += delta_time
        is_shot_due = self.seconds_since_fire >= AUTO_FIRE_INTERVAL
        if not is_shot_due:
            return

        self.seconds_since_fire = 0.0
        self.fire()

    def fire(self):
        if not self.can_fire:
            return

        target = self.local_player.aim_target
        if target is None:
            return

        nozzle_x, nozzle_y = self.local_player.held_item.nozzle_position()
        nozzle_to_target_y = target[1] - nozzle_y
        nozzle_to_target_x = target[0] - nozzle_x
        aim_radians = math.atan2(nozzle_to_target_y, nozzle_to_target_x)

        self.tank -= SHOT_COST
        self.seconds_since_shot = 0.0
        self.spawn_main_bullet(nozzle_x, nozzle_y, aim_radians)
        self.maybe_spawn_droplet(nozzle_x, nozzle_y, aim_radians)
        self.puffs.append(SprayPuff(nozzle_x, nozzle_y, aim_radians, self.puff_list))

    def spawn_main_bullet(self, nozzle_x, nozzle_y, aim_radians):
        direction = aim_radians + (random.random() - 0.5) * MAIN_SPREAD
        speed = BULLET_SPEED + random.random() * BULLET_SPEED_VARIANCE
        self.bullets.append(
            SprayBullet(nozzle_x, nozzle_y, direction, speed, BULLET_LIFESPAN, BULLET_SCALE, self.bullet_list)
        )

    def maybe_spawn_droplet(self, nozzle_x, nozzle_y, aim_radians):
        should_spawn = random.random() < DROPLET_CHANCE
        if not should_spawn:
            return

        direction = aim_radians + (random.random() - 0.5) * DROPLET_SPREAD
        speed = (BULLET_SPEED + random.random() * BULLET_SPEED_VARIANCE) * DROPLET_SPEED_FACTOR
        self.bullets.append(
            SprayBullet(nozzle_x, nozzle_y, direction, speed, DROPLET_LIFESPAN, DROPLET_SCALE, self.bullet_list)
        )

    def advance_projectiles(self, delta_time):
        for bullet in self.bullets:
            bullet.advance(delta_time)

        for puff in self.puffs:
            puff.advance(delta_time)
        self.remove_expired()

    def remove_expired(self):
        for bullet in [bullet for bullet in self.bullets if bullet.is_expired]:
            bullet.destroy()
            self.bullets.remove(bullet)

        for puff in [puff for puff in self.puffs if puff.is_expired]:
            puff.destroy()
            self.puffs.remove(puff)

    def cleanup_obstacle_hits(self):
        if self.obstacles is None:
            return

        for bullet in [bullet for bullet in self.bullets if self.hits_obstacle(bullet)]:
            bullet.destroy()
            self.bullets.remove(bullet)

    def hits_obstacle(self, bullet):
        return len(arcade.check_for_collision_with_list(bullet.sprite, self.obstacles.sprite_list)) > 0

    def cleanup_hits(self):
        if self.enemies is None:
            return

        for bullet in [bullet for bullet in self.bullets if self.hits_enemy(bullet)]:
            bullet.destroy()
            self.bullets.remove(bullet)

    def hits_enemy(self, bullet):
        hit_zombie = self.first_zombie_hit(bullet)
        if hit_zombie is None:
            return False

        self.damage_zombie(hit_zombie)
        return True

    def first_zombie_hit(self, bullet):
        for zombie in self.enemies.zombies:
            if arcade.check_for_collision(bullet.sprite, zombie.sprite):
                return zombie
        return None

    def damage_zombie(self, zombie):
        zombie.take_damage(BULLET_DAMAGE)
        if self.audio:
            self.audio.play_hit()
        if zombie.is_dead:
            self.enemies.zombies.remove(zombie)
            zombie.sprite.remove_from_sprite_lists()
            self.kills += 1
