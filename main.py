from pico2d import open_canvas, delay, close_canvas
import game_framework

import play_mode as start_mode

CANVAS_WIDTH = 1600
CANVAS_HEIGHT = 600

# BirdFlock reads this canvas size and reserves the upper flight corridor.
open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
game_framework.run(start_mode)
close_canvas()

