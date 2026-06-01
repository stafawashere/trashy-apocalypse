import arcade


class Camera:
    def __init__(self, player, map, screen, zoom=2.0):
        self.player = player
        self.map = map
        self.screen = screen
        self.camera = arcade.Camera2D()
        self.camera.zoom = zoom

    def use(self):
        self.camera.use()

    def update(self):
        half_view_width = self.screen.width / self.camera.zoom / 2
        half_view_height = self.screen.height / self.camera.zoom / 2

        min_center_x = half_view_width
        max_center_x = self.map.width - half_view_width
        min_center_y = half_view_height
        max_center_y = self.map.height - half_view_height

        clamped_center_x = min(max(self.player.sprite.center_x, min_center_x), max_center_x)
        clamped_center_y = min(max(self.player.sprite.center_y, min_center_y), max_center_y)

        self.camera.position = (clamped_center_x, clamped_center_y)
        return self.camera.position
