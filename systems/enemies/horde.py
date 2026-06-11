from systems.enemies.ai import ZombieChase
from systems.enemies.collision import ZombieCollision


class Horde:
    def __init__(self, local_player, spawner):
        self.spawner = spawner
        self.ai = ZombieChase(local_player, spawner)
        self.collision = ZombieCollision(local_player, spawner)

    @property
    def zombies(self):
        return self.spawner.zombies

    def chase(self):
        self.ai.update()

    def collide(self):
        self.collision.update()
