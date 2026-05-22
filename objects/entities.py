class Player:
    def __init__(self, name):
        self.name = name
        self.health = 100

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
