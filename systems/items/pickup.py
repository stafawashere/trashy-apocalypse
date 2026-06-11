import arcade


class Pickup:
    def __init__(self, local_player, spawner, held_list, audio=None):
        self.local_player = local_player
        self.spawner = spawner
        self.held_list = held_list
        self.audio = audio

    def update(self):
        if self.local_player.is_holding:
            return

        for item in self.spawner.items:
            is_touching_player = arcade.check_for_collision(self.local_player.sprite, item.sprite)
            if is_touching_player:
                self.collect(item)
                return

    def collect(self, item):
        self.spawner.items.remove(item)
        item.sprite.remove_from_sprite_lists()
        self.held_list.append(item.sprite)
        self.local_player.hold(item)
        if self.audio:
            self.audio.play_equip()
