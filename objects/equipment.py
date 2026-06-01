import arcade

class Equipment:
    def __init__(self, name, x=0, y=0, scale=0.3, offset_x=0, offset_y=0, sprite_list=None):
        self.name = name
        self.sprite = arcade.Sprite(f"assets/sprites/{name}.png", scale=scale)
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.offset_x = offset_x
        self.offset_y = offset_y

        if sprite_list is not None:
            sprite_list.append(self.sprite)

        self.equipped = False
    
    def equip(self):
        self.equipped = True

    def unequip(self):
        self.equipped = False