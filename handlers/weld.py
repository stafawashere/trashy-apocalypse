import arcade
from arcade.math import rotate_point


class Weld:
    def __init__(self, parent, equipment):
        self.parent = parent
        self.equipment = equipment

    def update(self):
        if not self.equipment.equipped and arcade.check_for_collision(self.parent.sprite, self.equipment.sprite):
            self.equipment.equip()

        if self.equipment.equipped:
            parent = self.parent.sprite
            equip = self.equipment.sprite

            if self.equipment.anchored:
                offset_x, offset_y = rotate_point(
                    self.equipment.offset_x, self.equipment.offset_y, 0, 0, parent.angle
                )
                equip.center_x = parent.center_x + offset_x
                equip.center_y = parent.center_y + offset_y
                equip.angle = parent.angle + self.equipment.rotation
            else:
                equip.center_x = parent.center_x + self.equipment.offset_x
                equip.center_y = parent.center_y + self.equipment.offset_y
