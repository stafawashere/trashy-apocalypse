import random
from entities import Item

MAX_SPAWN_ATTEMPTS = 50


class ItemSpawner:
    def __init__(self, camera, item_list, texture, name, obstacles=None):
        self.camera = camera
        self.item_list = item_list
        self.texture = texture
        self.name = name
        self.obstacles = obstacles
        self.items = []
        self.has_spawned = False

    def update(self):
        if self.has_spawned:
            return

        self.spawn()
        self.has_spawned = True

    def spawn(self):
        item = Item(self.name, self.texture, sprite_list=self.item_list)
        self.place_clear_of_obstacles(item)
        self.items.append(item)

    def place_clear_of_obstacles(self, item):
        half_width = item.sprite.width / 2
        half_height = item.sprite.height / 2

        for _ in range(MAX_SPAWN_ATTEMPTS):
            item.sprite.center_x, item.sprite.center_y = self.random_point_in_view(
                half_width, half_height
            )
            
            is_spot_clear = self.obstacles is None or not self.obstacles.would_collide(item.sprite, 0, 0)
            if is_spot_clear:
                return

    def random_point_in_view(self, sprite_half_width, sprite_half_height):
        center_x, center_y = self.camera.position()
        half_view_width = self.camera.half_view_width()
        half_view_height = self.camera.half_view_height()

        left = center_x - half_view_width + sprite_half_width
        right = center_x + half_view_width - sprite_half_width
        bottom = center_y - half_view_height + sprite_half_height
        top = center_y + half_view_height - sprite_half_height

        return random.uniform(left, right), random.uniform(bottom, top)
