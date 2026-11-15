"""Command-line interface for qrgen."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from qrcode.exceptions import DataOverflowError

from . import __version__
from .core import create_qr, is_link, resolve_output


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="qrgen",
        description="Convert a link into a permanent static QR-code PNG.",
    )
    parser.add_argument("link", help="URL to encode (e.g. https://example.com)")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        help="Output file or directory (default: ~/Downloads/<host>-qr.png)",
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)
    link = args.link.strip()

    if not is_link(link):
        print(
            "Error: provide a full URL with a scheme, "
            "e.g. https://example.com",
            file=sys.stderr,
        )
        return 2

    output = resolve_output(link, args.output)

    try:
        create_qr(link, output)
    except DataOverflowError:
        print(
            "Error: the link is too long to fit in a QR code.",
            file=sys.stderr,
        )
        return 1
    except OSError as err:
        print(f"Error: could not save file: {err}", file=sys.stderr)
        return 1

    print(f"QR code saved: {output.resolve()}")
    print("Static QR — works as long as the link does.")
    return 0
