class Aim:
    def __init__(self, local_player, camera):
        self.local_player = local_player
        self.camera = camera
        self.mouse_x = 0
        self.mouse_y = 0

    def on_mouse_motion(self, x, y):
        self.mouse_x = x
        self.mouse_y = y

    def update(self):
        if not self.local_player.is_holding:
            return
        target = self.camera.unproject((self.mouse_x, self.mouse_y))
        self.local_player.aim_at((target.x, target.y))
