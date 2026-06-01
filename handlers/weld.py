import arcade


class Weld:
    def __init__(self, parent, equipment):
        self.parent = parent
        self.equipment = equipment

    def update(self):
        if not self.equipment.equipped and arcade.check_for_collision(self.parent.sprite, self.equipment.sprite):
            self.equipment.equip()
        
        if self.equipment.equipped:
            self.equipment.sprite.center_x = self.parent.sprite.center_x + self.equipment.offset_x
            self.equipment.sprite.center_y = self.parent.sprite.center_y + self.equipment.offset_y
