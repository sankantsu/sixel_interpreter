from dataclasses import dataclass
import numpy as np
from numpy.typing import NDArray
from .constants import NUM_COLOR_REGISTERS
from .color import Color


@dataclass
class State:
    buf: NDArray[np.uint8]  # shape: (nrow, ncol, 3)
    cursor: tuple[int, int]  # row, col
    current_color: int
    color_registers: list[Color]

    def get_color(self) -> Color:
        return self.color_registers[self.current_color]

    @staticmethod
    def new(nrow: int, ncol: int) -> "State":
        buf = np.zeros((nrow, ncol, 3), dtype=np.uint8)
        cursor = (0, 0)
        current_color = 0
        color_registers = [Color(2, 0, 0, 0) for _ in range(NUM_COLOR_REGISTERS)]
        return State(buf, cursor, current_color, color_registers)
