from scenes.apocalypse import ApocalypseScene, MenuButton


class PauseScene(ApocalypseScene):
    def __init__(self, screen, on_resume, on_quit):
        super().__init__(screen, show_logo=True)
        self.resume_button = MenuButton(self, "RESUME", 336, on_resume)
        self.quit_button = MenuButton(self, "QUIT", 408, on_quit)
        self.buttons = [self.resume_button, self.quit_button]

    def update(self, delta_time):
        dt = self.advance_backdrop(delta_time)
        for button in self.buttons:
            button.update(dt)

    def draw(self):
        self.camera.use()
        self.draw_backdrop()
        self.draw_logo()
        self.draw_crt()
        for button in self.buttons:
            button.draw()

    def on_key_press(self, key):
        pass

    def on_key_release(self, key):
        pass

    def on_mouse_motion(self, x, y):
        self.mouse_x, self.mouse_y = x, y
        for button in self.buttons:
            button.hovered = button.hit(x, y)

    def on_mouse_press(self, x, y):
        for button in self.buttons:
            if button.hit(x, y):
                button.on_click()
                return

    def on_mouse_release(self):
        pass
