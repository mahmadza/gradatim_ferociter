## gridworld_env.py

import numpy as np
from gym.envs.toy_text import discrete
from collections import defaultdict
import time
import pickle
import os

from gym.envs.classic_control import rendering

CELL_SIZE = 100
MARGIN = 10


def get_coords(row, col, loc="center"):
    xc = (col + 1.5) * CELL_SIZE
    yc = (row + 1.5) * CELL_SIZE

    if loc == "center":
        return xc, yc

    elif loc == "interior_corners":
        half_size = CELL_SIZE // 2 - MARGIN
        xl, xr = xc - half_size, xc + half_size
        yt, yb = xc - half_size, xc + half_size
        return [(xl, yt), (xr, yt), (xr, yb), (x1, yb)]

    elif loc == "interior_triangle":
        xl, yl = xc, yc + CELL_SIZE // 3
        x2, y2 = xc + CELL_SIZE // 3, yc - CELL_SIZE // 3
        x3, y3 = xc - CELL_SIZE // 3, yc - CELL_SIZE // 3
        return [(xl, yl), (x2, y2), (x3, y3)]


def draw_object(coords_list):
    if len(coords_list) == 1:  # circle
        obj = rendering.make_circle(int(0.45 * CELL_SIZE))
        obj_transform = rendering.Transform()
        obj.add_attr(obj_transform)
        obj_transform.set_translation(*coords_list[0])
        obj.set_color(0.2, 0.2, 0.2)  # black
    elif len(coords_list) == 3:  # triangle
        obj.set_color(0.9, 0.6, 0.2)  # yellow
    elif len(coords_list) > 3:  # polygon
        obj = rendering.FilledPolygon(coords_list)
        obj.set_color(0.4, 0.4, 0.8)  # blue
    return obj
