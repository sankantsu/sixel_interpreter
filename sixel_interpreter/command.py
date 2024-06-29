from dataclasses import dataclass
from typing import TypeAlias
import numpy as np
from .constants import SIXEL_HEIGHT
from .color import Color
from .state import State


@dataclass
class PrintSixel:
    char: str

    def bit_pattern(self) -> list[bool]:
        bits = []
        x = ord(self.char) - 63
        for i in range(SIXEL_HEIGHT):
            bits.append(True if (x >> i) & 0x1 else False)
        return bits

    def update_state(self, state: State) -> None:
        r, c = state.cursor
        rgb = np.array(state.get_color().to_rgb())
        for i, on in enumerate(self.bit_pattern()):
            if on:
                state.buf[r + i][c][:] = rgb
        state.cursor = (r, c + 1)


@dataclass
class Repeat:
    char: str
    rep: int

    def update_state(self, state: State) -> None:
        cmd = PrintSixel(self.char)
        for _ in range(self.rep):
            cmd.update_state(state)


@dataclass
class SelectColor:
    id: int

    def update_state(self, state: State) -> None:
        state.current_color = self.id


@dataclass
class SetColor:
    id: int
    color: Color

    def update_state(self, state: State) -> None:
        state.color_registers[self.id] = self.color


class CarriageReturn:
    def update_state(self, state: State) -> None:
        r, c = state.cursor
        state.cursor = (r, 0)


class NewLine:
    def update_state(self, state: State) -> None:
        r, c = state.cursor
        state.cursor = (r + SIXEL_HEIGHT, 0)


# mypy currently have not yet supported PEP 695
# https://github.com/python/mypy/issues/15238
# type Command = PrintSixel | CarriageReturn | NewLine | SelectColor | SetColor

Command: TypeAlias = (
    PrintSixel | CarriageReturn | NewLine | SelectColor | SetColor | Repeat
)
