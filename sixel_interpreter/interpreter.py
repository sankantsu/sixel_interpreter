import numpy as np
from numpy.typing import NDArray
from .state import State
from .parser import parse


def execute(s: str) -> NDArray[np.uint8]:
    result = parse(s)
    state = State.new(result.img_height, result.img_width)
    for cmd in result.commands:
        cmd.update_state(state)
    return state.buf


def get_frames(s: str) -> list[NDArray[np.uint8]]:
    result = parse(s)
    state = State.new(result.img_height, result.img_width)
    frames = []
    for cmd in result.commands:
        frames.append(np.copy(state.buf))
        cmd.update_state(state)
    frames.append(np.copy(state.buf))
    return frames
