"""Time-based flight animation for the ten-bird flock."""

from pico2d import get_canvas_height, get_canvas_width, load_image


# Use the same world scale as the boy: 10 pixels represent 30 cm.
PIXEL_PER_METER = 10.0 / 0.3

# A representative cruising speed for a small bird.
FLY_SPEED_KMPH = 36.0
FLY_SPEED_MPS = FLY_SPEED_KMPH * 1000.0 / 3600.0
FLY_SPEED_PPS = FLY_SPEED_MPS * PIXEL_PER_METER

# One full 14-frame wingbeat advances the flock by two metres.
WINGBEAT_DISTANCE_M = 2.0
WINGBEATS_PER_SECOND = FLY_SPEED_MPS / WINGBEAT_DISTANCE_M

SPRITE_SHEET_WIDTH = 918
SPRITE_SHEET_HEIGHT = 506
SPRITE_COLUMNS = 5
SPRITE_ROWS = 3
FLIGHT_FRAME_COUNT = 14
FLIGHT_FRAMES_PER_SECOND = FLIGHT_FRAME_COUNT * WINGBEATS_PER_SECOND


class BirdFlock:
    """A placeholder flock that is filled out in the following commits."""

    def __init__(self):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.image = load_image('bird_animation.png')

    def update(self):
        pass

    def draw(self):
        pass
