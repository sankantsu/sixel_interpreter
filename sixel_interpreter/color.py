from dataclasses import dataclass


@dataclass
class Color:
    t: int
    x: int
    y: int
    z: int

    def __post_init__(self) -> None:
        self._validate()

    def _validate(self) -> None:
        def in_range(x: int, min: int, max: int) -> bool:
            return min <= x and x <= max

        match self.t:
            case 1:  # HSL
                ok = (
                    in_range(self.x, 0, 360)
                    and in_range(self.y, 0, 100)
                    and in_range(self.z, 0, 100)
                )
                if not ok:
                    raise ValueError("Invalid RGB value")
            case 2:  # RGB
                # rgb values are represented as percentage
                ok = (
                    in_range(self.x, 0, 100)
                    and in_range(self.y, 0, 100)
                    and in_range(self.z, 0, 100)
                )
                if not ok:
                    raise ValueError("Invalid RGB value")
            case _:
                raise ValueError(f"Invalid color type: {self.t}")

    def to_rgb(self) -> tuple[int, int, int]:
        match self.t:
            case 1:  # HSL
                raise NotImplementedError
            case 2:  # RGB
                r = int(255 * self.x / 100)
                g = int(255 * self.y / 100)
                b = int(255 * self.z / 100)
                return (r, g, b)
            case _:
                raise ValueError(f"Invalid color type {self.t}")
