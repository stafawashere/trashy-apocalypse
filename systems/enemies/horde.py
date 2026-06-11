from systems.enemies.ai import ZombieChase
from systems.enemies.collision import ZombieCollision


class Horde:
    def __init__(self, local_player, spawner, obstacles=None):
        self.spawner = spawner
        self.obstacles = obstacles
        self.ai = ZombieChase(local_player, spawner, obstacles)
        self.collision = ZombieCollision(local_player, spawner)

    @property
    def zombies(self):
        return self.spawner.zombies

    def chase(self):
        self.ai.update()

    def collide(self):
        self.collision.update()

    def respect_walls(self):
        if self.obstacles is None:
            return
        for zombie in self.zombies:
            self.obstacles.resolve(zombie.sprite)
