import sys
import argparse
from typing import Any
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sixel_interpreter import execute, get_frames


def show_image(data: str) -> None:
    _, ax = plt.subplots()
    img = execute(data)
    ax.imshow(img)
    plt.show()


def show_animation(data: str, **kwargs: Any) -> None:
    fig, ax = plt.subplots()
    frames = get_frames(data)
    ims = []
    for i, frame in enumerate(frames):
        im = ax.imshow(frame, animated=True)
        if i == 0:
            ax.imshow(frame)
        ims.append([im])
    _ = animation.ArtistAnimation(fig, ims, blit=True, repeat=False, **kwargs)
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", help="Sixel file to show (default: stdin)")
    parser.add_argument("--animation", action="store_true", help="Show animation")
    parser.add_argument("--interval", type=int, default=100, help="Animation interval")
    args = parser.parse_args()
    if args.file:
        with open(args.file) as f:
            data = f.read()
    else:
        data = sys.stdin.read()
    if args.animation:
        show_animation(data, interval=args.interval)
    else:
        show_image(data)


if __name__ == "__main__":
    main()
