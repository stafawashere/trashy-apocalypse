import arcade


class Camera:
    def __init__(self, local_player, map, screen, zoom=2.0):
        self.local_player = local_player
        self.map = map
        self.screen = screen
        self.base_zoom = zoom
        self.camera = arcade.Camera2D()
        self.camera.zoom = zoom

    def on_resize(self, width, height):
        self.camera.match_window()
        self.camera.zoom = self.base_zoom * self.screen.scale

    def use(self):
        self.camera.use()

    def position(self):
        return self.camera.position

    def unproject(self, screen_coordinate):
        return self.camera.unproject(screen_coordinate)

    def half_view_width(self):
        return self.screen.width / self.camera.zoom / 2

    def half_view_height(self):
        return self.screen.height / self.camera.zoom / 2

    def update(self):
        min_center_x = self.half_view_width()
        max_center_x = self.map.width - self.half_view_width()
        min_center_y = self.half_view_height()
        max_center_y = self.map.height - self.half_view_height()

        clamped_center_x = min(max(self.local_player.sprite.center_x, min_center_x), max_center_x)
        clamped_center_y = min(max(self.local_player.sprite.center_y, min_center_y), max_center_y)

        self.camera.position = (clamped_center_x, clamped_center_y)
        return self.camera.position
