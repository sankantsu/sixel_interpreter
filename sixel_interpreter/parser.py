from logging import getLogger
from dataclasses import dataclass
from .constants import SIXEL_HEIGHT
from .color import Color
from .command import (
    Command,
    PrintSixel,
    SetColor,
    SelectColor,
    NewLine,
    CarriageReturn,
    Repeat,
)

_logger = getLogger(__name__)


@dataclass
class ParseResult:
    img_height: int
    img_width: int
    commands: list[Command]


class Parser:
    def __init__(self, s: str) -> None:
        self._pos: int = 0
        self._s: str = s
        self._commands: list[Command] = []
        self._img_height: int = SIXEL_HEIGHT
        self._img_width: int = 0
        self._current_col: int = 0

    def _advance(self) -> None:
        self._pos += 1

    def _read(self) -> str:
        return self._s[self._pos]

    def _consume(self) -> str:
        c = self._read()
        self._advance()
        return c

    def _eos(self) -> bool:
        return self._pos >= len(self._s)

    def _add_command(self, command: Command) -> None:
        self._commands.append(command)

    def _parse_int(self) -> int:
        int_str = ""
        while not self._eos() and self._read().isdigit():
            int_str += self._consume()
        if not int_str:  # empty
            c = self._read()
            raise ValueError(f"Expected integer value, but found {c}")
        return int(int_str)

    def _parse_parameters(self, n: int) -> list[int]:
        params = []
        for i in range(n):
            assert self._consume() == ";"
            v = self._parse_int()
            params.append(v)
        return params

    def _parse_next_command(self) -> Command | None:
        c = self._consume()
        match c:
            case " " | "\n" | "\t":
                _logger.debug("Ignored whitespace")
                return None
            case "\x1b":
                nc = self._consume()
                if nc == "P":
                    nc = self._consume()
                    if nc != "q":
                        raise RuntimeError("Unknonw DCS detected!")
                    _logger.info("Started DCS")
                elif nc == "\\":
                    _logger.info("Ended DCS")
                return None
            case '"':
                _ = self._parse_int()
                _ = self._parse_parameters(3)
                _logger.warning("Ignored raster attributes")
                return None
            case "$":
                self._img_width = max(self._img_width, self._current_col)
                self._current_col = 0
                return CarriageReturn()
            case "-":
                self._img_width = max(self._img_width, self._current_col)
                self._current_col = 0
                self._img_height += SIXEL_HEIGHT
                return NewLine()
            case "#":
                id = self._parse_int()
                if self._eos() or self._read() != ";":
                    return SelectColor(id)
                else:
                    params = self._parse_parameters(4)
                    color = Color(*params)
                    return SetColor(id, color)
            case "!":
                rep = self._parse_int()
                nc = self._consume()
                if ord(nc) < 63 or 126 < ord(nc):
                    raise ValueError(f"Invalid sixel character {nc} at pos {self._pos}")
                self._current_col += rep
                return Repeat(nc, rep)
            case _:
                if ord(c) < 63 or 126 < ord(c):
                    raise ValueError(f"Invalid sixel character {c} at pos {self._pos}")
                self._current_col += 1
                return PrintSixel(c)

    def parse(self) -> ParseResult:
        while not self._eos():
            command = self._parse_next_command()
            if command:
                self._add_command(command)
        self._img_width = max(self._img_width, self._current_col)
        return ParseResult(
            img_height=self._img_height,
            img_width=self._img_width,
            commands=self._commands,
        )


def parse(s: str) -> ParseResult:
    parser = Parser(s)
    return parser.parse()
