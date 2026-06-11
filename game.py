import arcade
from objects import Screen, LocalPlayer, Map
from handlers import Movement, Camera, Boundary, Spawner, Pickup, Aim, ZombieSpawner, Horde, Blaster, Hud, Contact
from constants import WINDEX_TEXTURE, PLAYER_SPEED


screen = Screen(1000, 600, "Trashy Apocalypse")

class Process(arcade.Window):
    def __init__(self):
        super().__init__(screen.width, screen.height, screen.title, resizable=True)

    def setup(self):
        self.map_list = arcade.SpriteList()
        self.map = Map(sprite_list=self.map_list)

        self.player_list = arcade.SpriteList()
        self.local_player = LocalPlayer("localplayer", x=self.map.center[0], y=self.map.center[1], sprite_list=self.player_list)
        self.movement = Movement(self.local_player, player_speed=PLAYER_SPEED)
        self.camera = Camera(self.local_player, self.map, screen, zoom=2)
        self.boundary = Boundary(self.local_player, self.map)

        self.item_list = arcade.SpriteList()
        self.held_list = arcade.SpriteList()
        self.spawner = Spawner(self.camera, self.item_list, texture=WINDEX_TEXTURE, name="windex")
        self.pickup = Pickup(self.local_player, self.spawner, self.held_list)
        self.aim = Aim(self.local_player, self.camera)

        self.zombie_list = arcade.SpriteList()
        self.zombie_spawner = ZombieSpawner(self.map, self.zombie_list)
        self.horde = Horde(self.local_player, self.zombie_spawner)

        self.bullet_list = arcade.SpriteList()
        self.puff_list = arcade.SpriteList()
        self.blaster = Blaster(self.local_player, self.bullet_list, self.puff_list, enemies=self.zombie_spawner)
        self.contact = Contact(self.local_player, self.horde)
        self.hud = Hud(self.blaster, self.local_player, screen)

        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.map_list.draw()
        self.item_list.draw()
        self.zombie_list.draw()
        if self.local_player.is_facing_away:
            self.held_list.draw()
            self.player_list.draw()
        else:
            self.player_list.draw()
            self.held_list.draw()
        self.bullet_list.draw()
        self.puff_list.draw()

        self.hud.use()
        self.hud.draw()

    def on_update(self, delta_time: float):
        self.movement.update()
        self.player_list.update()
        self.boundary.update()
        self.camera.update()
        self.spawner.update()
        self.pickup.update()
        self.aim.update()
        self.zombie_spawner.update(delta_time)
        self.horde.chase()
        self.zombie_list.update()
        self.horde.collide()

        for zombie in self.zombie_spawner.zombies:
            zombie.update_animation(delta_time)

        self.contact.update(delta_time)
        self.local_player.update_animation(delta_time)
        self.blaster.update(delta_time)

    def on_key_press(self, key, modifiers):
        self.movement.on_key_press(key)

    def on_key_release(self, key, modifiers):
        self.movement.on_key_release(key)

    def on_mouse_motion(self, x, y, dx, dy):
        self.aim.on_mouse_motion(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.aim.on_mouse_motion(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        self.aim.on_mouse_motion(x, y)
        self.aim.update()
        self.blaster.on_mouse_press()

    def on_mouse_release(self, x, y, button, modifiers):
        self.blaster.on_mouse_release()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        if not hasattr(self, "camera"):
            return

        screen.resize(width, height)
        self.camera.on_resize(width, height)
        self.hud.on_resize()