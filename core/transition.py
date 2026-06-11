import arcade

FADE_DURATION = 0.35
_FADE_OUT = "fade_out"
_FADE_IN = "fade_in"


class FadeTransition:
    def __init__(self, duration=FADE_DURATION):
        self.duration = duration
        self.alpha = 0.0
        self.phase = None
        self.on_midpoint = None

    @property
    def is_active(self):
        return self.phase is not None

    @property
    def is_fading_out(self):
        return self.phase == _FADE_OUT

    def begin(self, on_midpoint):
        self.phase = _FADE_OUT
        self.on_midpoint = on_midpoint

    def begin_fade_in(self):
        self.phase = _FADE_IN
        self.alpha = 1.0

    def update(self, delta_time):
        if self.phase is None:
            return
        step = delta_time / self.duration
        if self.phase == _FADE_OUT:
            self.alpha = min(1.0, self.alpha + step)
            if self.alpha >= 1.0:
                self._switch_at_midpoint()
        else:
            self.alpha = max(0.0, self.alpha - step)
            if self.alpha <= 0.0:
                self.phase = None

    def _switch_at_midpoint(self):
        switch_scene = self.on_midpoint
        self.on_midpoint = None
        self.phase = _FADE_IN
        if switch_scene:
            switch_scene()

    def draw(self, width, height):
        if self.alpha <= 0.0:
            return
        overlay = (0, 0, 0, int(self.alpha * 255))
        arcade.draw_rect_filled(arcade.LBWH(0, 0, width, height), overlay)
