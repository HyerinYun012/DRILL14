"""Time-based flight animation for the ten-bird flock."""

from pico2d import get_canvas_height, get_canvas_width, load_image

import game_framework


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

DRAW_WIDTH = 72
DRAW_HEIGHT = 66

# Two staggered rows keep all ten birds readable near the top of the canvas.
FORMATION_OFFSETS = (
    (-180, 28), (-90, 28), (0, 28), (90, 28), (180, 28),
    (-225, -42), (-135, -42), (-45, -42), (45, -42), (135, -42),
)
FRAME_PHASE_OFFSETS = (0, 3, 6, 9, 12, 2, 5, 8, 11, 13)


def frame_rectangle(frame_index):
    """Return an exact Pico2D clip rectangle for one of the 14 frames."""
    frame_index %= FLIGHT_FRAME_COUNT
    row_from_top, column = divmod(frame_index, SPRITE_COLUMNS)

    left = column * SPRITE_SHEET_WIDTH // SPRITE_COLUMNS
    right = (column + 1) * SPRITE_SHEET_WIDTH // SPRITE_COLUMNS
    top = row_from_top * SPRITE_SHEET_HEIGHT // SPRITE_ROWS
    next_top = (row_from_top + 1) * SPRITE_SHEET_HEIGHT // SPRITE_ROWS

    width = right - left
    height = next_top - top
    bottom = SPRITE_SHEET_HEIGHT - next_top
    return left, bottom, width, height


class BirdFlock:
    """A placeholder flock that is filled out in the following commits."""

    def __init__(self):
        self.canvas_width = get_canvas_width()
        self.canvas_height = get_canvas_height()
        self.image = load_image('bird_animation.png')
        horizontal_extent = max(abs(x) for x, _ in FORMATION_OFFSETS)
        self.left_bound = horizontal_extent + DRAW_WIDTH / 2
        self.right_bound = (
            self.canvas_width - horizontal_extent - DRAW_WIDTH / 2
        )
        self.x = self.left_bound
        self.y = self.canvas_height - 100.0
        self.direction = 1
        self.frame = 0.0

    def update(self):
        elapsed = game_framework.frame_time
        self.frame = (
            self.frame + FLIGHT_FRAMES_PER_SECOND * elapsed
        ) % FLIGHT_FRAME_COUNT
        self.x += self.direction * FLY_SPEED_PPS * elapsed
        self._reflect_at_edges()

    def _reflect_at_edges(self):
        """Reflect overshoot so a slow frame cannot change flight distance."""
        while self.x < self.left_bound or self.x > self.right_bound:
            if self.x > self.right_bound:
                self.x = 2 * self.right_bound - self.x
                self.direction = -1
            elif self.x < self.left_bound:
                self.x = 2 * self.left_bound - self.x
                self.direction = 1

    def draw(self):
        flip = '' if self.direction > 0 else 'h'

        for (offset_x, offset_y), phase in zip(
                FORMATION_OFFSETS, FRAME_PHASE_OFFSETS):
            frame_index = int(self.frame + phase) % FLIGHT_FRAME_COUNT
            left, bottom, width, height = frame_rectangle(frame_index)
            bird_x = self.x + self.direction * offset_x
            bird_y = self.y + offset_y

            self.image.clip_composite_draw(
                left, bottom, width, height,
                0, flip,
                bird_x, bird_y, DRAW_WIDTH, DRAW_HEIGHT
            )
