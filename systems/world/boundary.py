class Boundary:
    def __init__(self, local_player, map):
        self.local_player = local_player
        self.map = map

    def update(self):
        player_sprite = self.local_player.sprite
        half_player_width = player_sprite.width / 2
        half_player_height = player_sprite.height / 2

        min_x = half_player_width
        max_x = self.map.width - half_player_width
        min_y = half_player_height
        max_y = self.map.height - half_player_height

        if player_sprite.center_x < min_x:
            player_sprite.center_x = min_x
        elif player_sprite.center_x > max_x:
            player_sprite.center_x = max_x

        if player_sprite.center_y < min_y:
            player_sprite.center_y = min_y
        elif player_sprite.center_y > max_y:
            player_sprite.center_y = max_y
