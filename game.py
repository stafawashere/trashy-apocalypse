import arcade
from .objects import Screen


screen = Screen(1000, 600, "DeepClean")


class Process(arcade.Window):
    def __init__(self):
        super().__init__(screen.width, screen.height, screen.title)
        self.setup()

    def setup(self):
        arcade.set_background_color(arcade.color.BLACK)
        # initialize player, weapon, zombies, and other game state

    def on_draw(self):
        arcade.start_render()
        # draw sprites, UI, game info, and shit

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