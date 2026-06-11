import arcade
from constants import CONTACT_DAMAGE, DAMAGE_COOLDOWN_SECONDS


class Contact:
    def __init__(self, local_player, horde):
        self.local_player = local_player
        self.horde = horde
        self.seconds_until_vulnerable = 0.0

    def update(self, delta_time):
        if self.seconds_until_vulnerable > 0:
            self.seconds_until_vulnerable -= delta_time
            return

        if self.is_touching_zombie():
            self.local_player.take_damage(CONTACT_DAMAGE)
            self.seconds_until_vulnerable = DAMAGE_COOLDOWN_SECONDS

    def is_touching_zombie(self):
        for zombie in self.horde.zombies:
            if arcade.check_for_collision(self.local_player.sprite, zombie.sprite):
                return True
        return False
