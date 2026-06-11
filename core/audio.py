import arcade

from constants import (
    MUSIC_PATH,
    WIND_PATH,
    CLICK_PATH,
    CLICK_VOLUME,
    HOVER_PATH,
    HOVER_VOLUME,
    WALK_PATH,
    WALK_VOLUME,
    WALK_SOUND_SPEED,
    SPRAY_PATH,
    SPRAY_VOLUME,
    EQUIP_PATH,
    EQUIP_VOLUME,
    HIT_PATH,
    HIT_VOLUME,
    DAMAGE_PATH,
    DAMAGE_VOLUME,
    GAMEOVER_SFX_PATH,
    GAMEOVER_SFX_VOLUME,
    HIT_SOUND_MIN_INTERVAL,
    AUDIO_FADE_RATE,
    WALK_FADE_RATE,
    SPRAY_FADE_RATE,
)


class FadingTrack:
    def __init__(self, path, loop=True, speed=1.0, fade_rate=AUDIO_FADE_RATE):
        self.sound = arcade.load_sound(path, streaming=True)
        self.loop = loop
        self.speed = speed
        self.fade_rate = fade_rate
        self.player = None
        self.volume = 0.0
        self.target_volume = 0.0

    @property
    def is_silent(self):
        return self.volume <= 0.001 and self.target_volume <= 0.001

    def fade_to(self, target_volume):
        self.target_volume = target_volume
        is_starting = self.player is None and target_volume > 0.0
        if is_starting:
            self.player = arcade.play_sound(
                self.sound, volume=self._perceptual(self.volume), loop=self.loop, speed=self.speed
            )

    def update(self, delta_time):
        if self.player is None:
            return
        step = min(1.0, delta_time * self.fade_rate)
        self.volume += (self.target_volume - self.volume) * step
        self.player.volume = self._perceptual(self.volume)

    @staticmethod
    def _perceptual(volume):
        return volume * volume


class AudioManager:
    def __init__(self):
        self.music = FadingTrack(MUSIC_PATH)
        self.wind = FadingTrack(WIND_PATH)
        self.walk = FadingTrack(WALK_PATH, speed=WALK_SOUND_SPEED, fade_rate=WALK_FADE_RATE)
        self.spray = FadingTrack(SPRAY_PATH, fade_rate=SPRAY_FADE_RATE)
        self.click_sound = arcade.load_sound(CLICK_PATH)
        self.hover_sound = arcade.load_sound(HOVER_PATH)
        self.equip_sound = arcade.load_sound(EQUIP_PATH)
        self.hit_sound = arcade.load_sound(HIT_PATH)
        self.damage_sound = arcade.load_sound(DAMAGE_PATH)
        self.game_over_sound = arcade.load_sound(GAMEOVER_SFX_PATH)
        self.seconds_since_hit = HIT_SOUND_MIN_INTERVAL

    def set_levels(self, music_volume, wind_volume):
        self.music.fade_to(music_volume)
        self.wind.fade_to(wind_volume)

    def set_walking(self, is_walking):
        self.walk.fade_to(WALK_VOLUME if is_walking else 0.0)

    def set_spraying(self, is_spraying):
        self.spray.fade_to(SPRAY_VOLUME if is_spraying else 0.0)

    def play_click(self):
        arcade.play_sound(self.click_sound, volume=CLICK_VOLUME)

    def play_hover(self):
        arcade.play_sound(self.hover_sound, volume=HOVER_VOLUME)

    def play_game_over(self):
        arcade.play_sound(self.game_over_sound, volume=GAMEOVER_SFX_VOLUME)

    def play_damage(self):
        arcade.play_sound(self.damage_sound, volume=DAMAGE_VOLUME)

    def play_equip(self):
        arcade.play_sound(self.equip_sound, volume=EQUIP_VOLUME)

    def play_hit(self):
        is_too_soon = self.seconds_since_hit < HIT_SOUND_MIN_INTERVAL
        if is_too_soon:
            return
        self.seconds_since_hit = 0.0
        arcade.play_sound(self.hit_sound, volume=HIT_VOLUME)

    def update(self, delta_time):
        self.seconds_since_hit += delta_time
        self.music.update(delta_time)
        self.wind.update(delta_time)
        self.walk.update(delta_time)
        self.spray.update(delta_time)
