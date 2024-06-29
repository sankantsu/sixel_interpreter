import sys
import argparse
from typing import Any
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from sixel_interpreter import execute, get_frames


def show_image(data: str, *, out: str | None) -> None:
    _, ax = plt.subplots()
    img = execute(data)
    ax.imshow(img)
    if out:
        plt.savefig(out)
    plt.show()


def show_animation(data: str, *, out: str | None, **kwargs: Any) -> None:
    fig, ax = plt.subplots()
    frames = get_frames(data)
    ims = []
    for i, frame in enumerate(frames):
        im = ax.imshow(frame, animated=True)
        if i == 0:
            ax.imshow(frame)
        ims.append([im])
    ani = animation.ArtistAnimation(fig, ims, blit=True, repeat=False, **kwargs)
    if out:
        ani.save(out)
    plt.show()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("file", nargs="?", help="Sixel file to show (default: stdin)")
    parser.add_argument("--animation", action="store_true", help="Show animation")
    parser.add_argument("--interval", type=int, default=100, help="Animation interval")
    parser.add_argument("--out", help="Filename to save image/animation")
    args = parser.parse_args()
    if args.file:
        with open(args.file) as f:
            data = f.read()
    else:
        data = sys.stdin.read()
    if args.animation:
        show_animation(data, out=args.out, interval=args.interval)
    else:
        show_image(data, out=args.out)


if __name__ == "__main__":
    main()
