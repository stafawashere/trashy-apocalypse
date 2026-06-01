import arcade


class Map:
    def __init__(self, sprite_list=None):
        self.name = "background"

        self.sprite = arcade.Sprite("assets/background.png")
        self.sprite.center_x = self.sprite.width / 2
        self.sprite.center_y = self.sprite.height / 2

        self.width = self.sprite.width
        self.height = self.sprite.height
        self.center = (self.sprite.center_x, self.sprite.center_y)

        if sprite_list is not None:
            sprite_list.append(self.sprite)
