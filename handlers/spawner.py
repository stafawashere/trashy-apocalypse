import random

from objects import Item


class Spawner:
    def __init__(self, camera, item_list, texture, name):
        self.camera = camera
        self.item_list = item_list
        self.texture = texture
        self.name = name
        self.items = []
        self.has_spawned = False

    def update(self):
        if self.has_spawned:
            return
        self.spawn()
        self.has_spawned = True

    def spawn(self):
        item = Item(self.name, self.texture, sprite_list=self.item_list)
        item.sprite.center_x, item.sprite.center_y = self.random_point_in_view(
            item.sprite.width / 2, item.sprite.height / 2
        )
        self.items.append(item)

    def random_point_in_view(self, sprite_half_width, sprite_half_height):
        center_x, center_y = self.camera.position()
        half_view_width = self.camera.half_view_width()
        half_view_height = self.camera.half_view_height()

        left = center_x - half_view_width + sprite_half_width
        right = center_x + half_view_width - sprite_half_width
        bottom = center_y - half_view_height + sprite_half_height
        top = center_y + half_view_height - sprite_half_height

        return random.uniform(left, right), random.uniform(bottom, top)
