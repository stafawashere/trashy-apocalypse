import arcade
from entities import LocalPlayer
from systems import (
    Movement,
    Camera,
    Boundary,
    ItemSpawner,
    Pickup,
    Aim,
    ZombieSpawner,
    Horde,
    Blaster,
    Contact,
    Map,
    Obstacles,
)
from ui import Hud, Crosshair
from constants import WINDEX_TEXTURE, WINDEX_NAME, PLAYER_SPEED


class GameplayScene:
    def __init__(self, screen, audio=None):
        self.screen = screen
        self.audio = audio
        self._build_world()
        self._build_player()
        self._build_items()
        self._build_enemies()
        self._build_combat()
        self._build_hud()
        arcade.set_background_color(arcade.color.BLACK)

    def _build_world(self):
        self.map_list = arcade.SpriteList()
        self.map = Map(sprite_list=self.map_list)

    def _build_player(self):
        self.player_list = arcade.SpriteList()
        self.local_player = LocalPlayer(
            x=self.map.center[0],
            y=self.map.center[1],
            sprite_list=self.player_list,
        )
        
        self.movement = Movement(self.local_player, player_speed=PLAYER_SPEED)
        self.camera = Camera(self.local_player, self.map, self.screen, zoom=2)
        self.boundary = Boundary(self.local_player, self.map)
        self.obstacles = Obstacles(self.local_player)

    def _build_items(self):
        self.item_list = arcade.SpriteList()
        self.held_list = arcade.SpriteList()
        self.spawner = ItemSpawner(self.camera, self.item_list, texture=WINDEX_TEXTURE, name=WINDEX_NAME, obstacles=self.obstacles)
        self.pickup = Pickup(self.local_player, self.spawner, self.held_list, audio=self.audio)
        self.aim = Aim(self.local_player, self.camera)

    def _build_enemies(self):
        self.zombie_list = arcade.SpriteList()
        self.zombie_spawner = ZombieSpawner(self.map, self.zombie_list, self.obstacles)
        self.horde = Horde(self.local_player, self.zombie_spawner, self.obstacles)

    def _build_combat(self):
        self.bullet_list = arcade.SpriteList()
        self.puff_list = arcade.SpriteList()
        self.blaster = Blaster(self.local_player, self.bullet_list, self.puff_list, enemies=self.zombie_spawner, audio=self.audio, obstacles=self.obstacles)
        self.contact = Contact(self.local_player, self.horde, audio=self.audio)

    def _build_hud(self):
        self.hud = Hud(self.blaster, self.local_player, self.screen)
        self.crosshair = Crosshair(self.local_player, self.blaster, self.screen)

    def draw(self):
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
        self.crosshair.draw()

    def update(self, delta_time):
        self.movement.update()
        self.player_list.update()
        self.obstacles.update()
        self.boundary.update()
        self.camera.update()
        self.spawner.update()
        self.pickup.update()
        self.aim.update()
        self.zombie_spawner.update(delta_time)
        self.horde.chase()
        self.zombie_list.update()
        self.horde.collide()
        self.horde.respect_walls()

        for zombie in self.zombie_spawner.zombies:
            zombie.update_animation(delta_time)

        self.contact.update(delta_time)
        self.local_player.update_animation(delta_time)
        self.blaster.update(delta_time)
        self.crosshair.update(delta_time)

    def on_key_press(self, key):
        self.movement.on_key_press(key)

    def on_key_release(self, key):
        self.movement.on_key_release(key)

    def on_mouse_motion(self, x, y):
        self.aim.on_mouse_motion(x, y)
        self.crosshair.on_mouse_motion(x, y)

    def on_mouse_press(self, x, y):
        self.aim.on_mouse_motion(x, y)
        self.crosshair.on_mouse_motion(x, y)
        self.aim.update()
        self.blaster.on_mouse_press()

    def on_mouse_release(self):
        self.blaster.on_mouse_release()

    def on_resize(self, width, height):
        self.screen.resize(width, height)
        self.camera.on_resize(width, height)
        self.hud.on_resize()
