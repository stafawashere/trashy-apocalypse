import arcade

class Player:
    def __init__(self, name, x=0, y=0, sprite_list=None):
        self.name = name
        self.health = 100
        self.state = "idle"

        self.sprite = arcade.Sprite("assets/sprites/player.png", scale=0.1)
        self.sprite.center_x = x
        self.sprite.center_y = y

        if sprite_list is not None:
            sprite_list.append(self.sprite)

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0
        return self.health
    
    def heal(self, amount):
        self.health += amount
        if self.health > 100:
            self.health = 100
        return self.health


class Zombie:
    def __init__(self, x=0, y=0, sprite_list=None):
        self.name = "zombie"
        self.health = 100
        self.state = "chasing"

        self.sprite = arcade.Sprite("assets/sprites/player.png", scale=0.1)
        self.sprite.center_x = x
        self.sprite.center_y = y
        self.sprite.color = (255, 60, 60)

        if sprite_list is not None:
            sprite_list.append(self.sprite)