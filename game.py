import arcade
from core import Screen
from scenes import GameplayScene


screen = Screen(1000, 600, "Trashy Apocalypse")


class Game(arcade.Window):
    def __init__(self):
        super().__init__(screen.width, screen.height, screen.title, resizable=True)

    def setup(self):
        self.scene = GameplayScene(screen)

    def on_draw(self):
        self.clear()
        self.scene.draw()

    def on_update(self, delta_time):
        self.scene.update(delta_time)

    def on_key_press(self, key, modifiers):
        self.scene.on_key_press(key)

    def on_key_release(self, key, modifiers):
        self.scene.on_key_release(key)

    def on_mouse_motion(self, x, y, dx, dy):
        self.scene.on_mouse_motion(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.scene.on_mouse_motion(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        self.scene.on_mouse_press(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        self.scene.on_mouse_release()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        if hasattr(self, "scene"):
            self.scene.on_resize(width, height)
