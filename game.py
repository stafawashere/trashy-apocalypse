import arcade
from objects.__init__ import Screen, Player


screen = Screen(1000, 600, "DeepClean")


class Process(arcade.Window):
    def __init__(self):
        super().__init__(screen.width, screen.height, screen.title)
        self.setup()

    def setup(self):
        self.player_list = arcade.SpriteList()
        self.player = Player("player", x=screen.center[0], y=screen.center[1], sprite_list=self.player_list)
        
        arcade.set_background_color(arcade.color.BLACK)
        # initialize player, weapon, zombies, and other game state

    def on_draw(self):
        self.clear()
        self.player_list.draw()

    def on_update(self, delta_time: float):
        
        # update player movement, zombie shitty AI, bullets, collisions
        pass

    def on_key_press(self, key, modifiers):
        # player input for movement, shooting, and restart
        pass

    def on_key_release(self, key, modifiers):
        # sp movement or adjust controls when keys are released.
        pass


def main():
    window = Process()
    arcade.run()


if __name__ == "__main__":
    main()