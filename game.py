import arcade
from core import Screen
from scenes import GameplayScene, TitleScene, PauseScene


screen = Screen(1000, 600, "Trashy Apocalypse")


class Game(arcade.Window):
    def __init__(self):
        super().__init__(screen.width, screen.height, screen.title, resizable=True)
        self.gameplay = None

    def setup(self):
        self.scene = TitleScene(screen, on_start=self.start_gameplay)

    def start_gameplay(self):
        self.gameplay = GameplayScene(screen)
        self.scene = self.gameplay

    def pause_gameplay(self):
        self.scene = PauseScene(screen, on_resume=self.resume_gameplay, on_quit=self.quit_game)

    def resume_gameplay(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.scene = self.gameplay

    def quit_game(self):
        self.close()

    def on_draw(self):
        self.clear()
        self.scene.draw()

    def on_update(self, delta_time):
        self.scene.update(delta_time)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.ESCAPE:
            if isinstance(self.scene, GameplayScene):
                self.pause_gameplay()
                return
            if isinstance(self.scene, PauseScene):
                self.resume_gameplay()
                return
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
