import arcade


class Movement:
    def __init__(self, player, player_speed=4):
        self.player = player
        self.player_speed = player_speed
        self.keys_held = {
            "left": False,
            "right": False,
            "up": False,
            "down": False,
        }

    def on_key_press(self, key):
        if key in (arcade.key.A, arcade.key.LEFT):
            self.keys_held["left"] = True
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.keys_held["right"] = True
        elif key in (arcade.key.W, arcade.key.UP):
            self.keys_held["up"] = True
        elif key in (arcade.key.S, arcade.key.DOWN):
            self.keys_held["down"] = True

        self.update_player_velocity()

    def on_key_release(self, key):
        if key in (arcade.key.A, arcade.key.LEFT):
            self.keys_held["left"] = False
        elif key in (arcade.key.D, arcade.key.RIGHT):
            self.keys_held["right"] = False
        elif key in (arcade.key.W, arcade.key.UP):
            self.keys_held["up"] = False
        elif key in (arcade.key.S, arcade.key.DOWN):
            self.keys_held["down"] = False

        self.update_player_velocity()

    def update_player_velocity(self):
        move_x = 0
        move_y = 0

        if self.keys_held["left"]:
            move_x -= self.player_speed
        if self.keys_held["right"]:
            move_x += self.player_speed
        if self.keys_held["up"]:
            move_y += self.player_speed
        if self.keys_held["down"]:
            move_y -= self.player_speed

        self.player.sprite.change_x = move_x
        self.player.sprite.change_y = move_y
        return move_x, move_y

    def update(self):
        self.update_player_velocity()
