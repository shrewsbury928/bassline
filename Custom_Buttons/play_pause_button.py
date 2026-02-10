from kivy.uix.widget import Widget
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, Triangle, RoundedRectangle, PushMatrix, PopMatrix, Translate, Scale
from kivy.animation import Animation


class PlayPauseButton(ButtonBehavior, Widget):
    """A play/pause button that crossfades a triangle (play) into two bars (pause).

    Usage: import the class and add it to your UI, or load the accompanying KV snippet.
    """
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.is_playing = False  # False -> show triangle (play). True -> show bars (pause)
        # visual padding
        self.pad = 8

        # Colors: triangle and bars share color but separate alpha for animation
        with self.canvas:
            # triangle color + triangle instruction
            self._tri_color = Color(1, 1, 1, 1)
            self._triangle = Triangle(points=self._triangle_points(0, 0, 0, 0))

            # pause bars color, start invisible
            self._bar_color = Color(1, 1, 1, 0)  # a=0 initially so bars hidden
            self._left_bar = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[4])
            self._right_bar = RoundedRectangle(pos=(0, 0), size=(0, 0), radius=[4])

        # update drawings when size/pos change
        self.bind(pos=self._update_graphics, size=self._update_graphics)

    def _triangle_points(self, x, y, w, h):
        # compute triangle pointing to the right
        pad = self.pad
        left = x + pad
        right = x + w - pad
        bottom = y + pad
        top = y + h - pad
        mid_y = y + h / 2
        # triangle vertices: (left, bottom), (left, top), (right, mid_y)
        return [left, bottom, left, top, right, mid_y]

    def _update_graphics(self, *a):
        x, y = self.pos
        w, h = self.size
        # update triangle
        self._triangle.points = self._triangle_points(x, y, w, h)

        # compute bars for pause icon
        bar_w = max(6, (w - 3 * self.pad) / 4)  # width of each bar
        bar_h = h - 2 * self.pad
        left_bar_x = x + self.pad
        right_bar_x = x + self.pad + bar_w + self.pad
        bar_y = y + self.pad
        self._left_bar.pos = (left_bar_x, bar_y)
        self._left_bar.size = (bar_w, bar_h)
        self._right_bar.pos = (right_bar_x, bar_y)
        self._right_bar.size = (bar_w, bar_h)

    def on_press(self):
        # IMPORTANT: Call parent to fire the event that bound callbacks listen to
        # The bound callback will handle state changes via set_playing()
        super().on_press()
        print(f"PlayPauseButton pressed -> is_playing={self.is_playing}")

    # animation attributes (simple attributes used by Animation)
    _tri_a = 1.0
    _bar_a = 0.0
    scale = 1.0

    def _anim_progress(self, animation, widget, progression):
        # update the color alphas and the transform scale
        ta = max(0.0, min(1.0, getattr(self, '_tri_a', 1.0)))
        ba = max(0.0, min(1.0, getattr(self, '_bar_a', 0.0)))
        # apply to Color instructions (Color.rgba = (r,g,b,a))
        self._tri_color.a = ta
        self._bar_color.a = ba
        # no transforms here — keep it simple and reliable for clicks

    def set_playing(self, playing: bool, animate=True):
        """Set the playing state and optionally animate the transition"""
        old_state = self.is_playing
        self.is_playing = bool(playing)
        
        if animate and old_state != self.is_playing:
            # Animate the transition
            if self.is_playing:
                # triangle → fade out, bars fade in
                anim = Animation(_tri_a=0, _bar_a=1, d=0.18, t='out_quad')
            else:
                # bars → fade out, triangle fade in
                anim = Animation(_tri_a=1, _bar_a=0, d=0.18, t='out_quad')
            anim.bind(on_progress=self._anim_progress)
            anim.start(self)
        else:
            # Instantly set without animation
            self._tri_color.a = 0.0 if self.is_playing else 1.0
            self._bar_color.a = 1.0 if self.is_playing else 0.0

__all__ = ['PlayPauseButton']