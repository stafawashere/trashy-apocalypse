import arcade
from objects.__init__ import Screen, Player, Map
from handlers import Movement, Rotation, Camera, Boundary, Horde


screen = Screen(1000, 600, "Trashy Apocalypse")


class Process(arcade.Window):
    def __init__(self):
        super().__init__(screen.width, screen.height, screen.title)
        self.setup()

    def setup(self):
        self.map_list = arcade.SpriteList()
        self.map = Map(sprite_list=self.map_list)

        self.player_list = arcade.SpriteList()
        self.player = Player("player", x=self.map.center[0], y=self.map.center[1], sprite_list=self.player_list)
        self.movement = Movement(self.player, player_speed=4)
        self.camera = Camera(self.player, self.map, screen, zoom=2)
        self.rotation = Rotation(self.player, self.camera, angle_offset=0)
        self.boundary = Boundary(self.player, self.map)

        self.zombie_list = arcade.SpriteList()
        self.horde = Horde(self.player, self.map, player_speed=4, spawn_interval=10, sprite_list=self.zombie_list)

        arcade.set_background_color(arcade.color.BLACK)
        # initialize player, weapon, zombies, and other game state

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.map_list.draw()
        self.zombie_list.draw()
        self.player_list.draw()

    def on_update(self, delta_time: float):
        self.movement.update()
        self.player_list.update()
        self.boundary.update()
        self.camera.update()
        self.rotation.update()
        self.horde.update(delta_time)
        # bullets, damage

    def on_key_press(self, key, modifiers):
        self.movement.on_key_press(key)

    def on_key_release(self, key, modifiers):
        self.movement.on_key_release(key)

    def on_mouse_motion(self, x, y, dx, dy):
        self.rotation.on_mouse_motion(x, y)


def main():
    window = Process()
    arcade.run()


if __name__ == "__main__":
    main()