import arcade
from core import Screen, AudioManager, record_score, FadeTransition
from ui import Pointer
from constants import (
    MUSIC_VOLUME_TITLE,
    MUSIC_VOLUME_GAMEPLAY,
    MUSIC_VOLUME_PAUSE,
    MUSIC_VOLUME_GAMEOVER,
    WIND_VOLUME_AMBIENT,
    WIND_VOLUME_SILENT,
)
from scenes import GameplayScene, TitleScene, PauseScene, GameOverScene


screen = Screen(1000, 600, "Trashy Apocalypse")


class Game(arcade.Window):
    def __init__(self):
        super().__init__(screen.width, screen.height, screen.title, resizable=True)
        self.gameplay = None
        self.audio = AudioManager()
        self.transition = FadeTransition()
        self.pointer = Pointer(screen)
        self.set_mouse_visible(False)

    def setup(self):
        self.scene = TitleScene(screen, on_start=self.start_gameplay, audio=self.audio)
        self.transition.begin_fade_in()

    def _transition_to(self, switch_scene):
        if self.transition.is_fading_out:
            return
        self.transition.begin(switch_scene)

    def start_gameplay(self):
        self.audio.play_click()
        self._transition_to(self._show_gameplay)

    def _show_gameplay(self):
        self.gameplay = GameplayScene(screen, audio=self.audio)
        self.scene = self.gameplay

    def pause_gameplay(self):
        self._transition_to(self._show_pause)

    def _show_pause(self):
        self.scene = PauseScene(screen, on_resume=self.resume_gameplay, on_quit=self.quit_game, audio=self.audio)

    def resume_gameplay(self):
        self.audio.play_click()
        self._transition_to(self._show_resumed_gameplay)

    def _show_resumed_gameplay(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.scene = self.gameplay

    def game_over(self):
        self.audio.play_game_over()
        self._transition_to(self._show_game_over)

    def _show_game_over(self):
        kills = self.gameplay.blaster.kills
        high_score = record_score(kills)
        self.scene = GameOverScene(screen, on_back=self.back_to_menu, kills=kills, high_score=high_score, audio=self.audio)

    def back_to_menu(self):
        self.audio.play_click()
        self._transition_to(self._show_menu)

    def _show_menu(self):
        arcade.set_background_color(arcade.color.BLACK)
        self.scene = TitleScene(screen, on_start=self.start_gameplay, audio=self.audio)

    def quit_game(self):
        self.audio.play_click()
        self.close()

    def _scene_audio_levels(self):
        if isinstance(self.scene, GameplayScene):
            return MUSIC_VOLUME_GAMEPLAY, WIND_VOLUME_SILENT
        if isinstance(self.scene, PauseScene):
            return MUSIC_VOLUME_PAUSE, WIND_VOLUME_SILENT
        if isinstance(self.scene, GameOverScene):
            return MUSIC_VOLUME_GAMEOVER, WIND_VOLUME_AMBIENT
        return MUSIC_VOLUME_TITLE, WIND_VOLUME_AMBIENT

    def on_draw(self):
        self.clear()
        self.scene.draw()
        self.default_camera.use()
        self.transition.draw(self.width, self.height)
        if not self._is_crosshair_active():
            self.pointer.draw()

    def _is_crosshair_active(self):
        return isinstance(self.scene, GameplayScene) and self.scene.crosshair.is_active

    def on_update(self, delta_time):
        self.transition.update(delta_time)
        self.scene.update(delta_time)
        is_player_dead = isinstance(self.scene, GameplayScene) and self.scene.local_player.health <= 0
        if is_player_dead and not self.transition.is_active:
            self.game_over()
        self.audio.set_levels(*self._scene_audio_levels())
        self.audio.set_walking(self._is_player_walking())
        self.audio.set_spraying(self._is_player_spraying())
        self.audio.update(delta_time)

    def _is_player_walking(self):
        if not isinstance(self.scene, GameplayScene):
            return False
        sprite = self.scene.local_player.sprite
        return sprite.change_x != 0 or sprite.change_y != 0

    def _is_player_spraying(self):
        if not isinstance(self.scene, GameplayScene):
            return False
        return self.scene.blaster.is_spraying

    def on_key_press(self, key, modifiers):
        if self.transition.is_fading_out:
            return
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
        self.pointer.on_mouse_motion(x, y)
        self.scene.on_mouse_motion(x, y)

    def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
        self.pointer.on_mouse_motion(x, y)
        self.scene.on_mouse_motion(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        self.pointer.on_mouse_motion(x, y)
        self.scene.on_mouse_press(x, y)

    def on_mouse_release(self, x, y, button, modifiers):
        self.scene.on_mouse_release()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        if hasattr(self, "scene"):
            self.scene.on_resize(width, height)
