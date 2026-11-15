"""Core logic: URL validation, filename generation, QR creation."""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse

import qrcode
from qrcode.constants import ERROR_CORRECT_H
from qrcode.exceptions import DataOverflowError

# Schemes we consider "linkable" — keeps javascript:, data:, etc. out.
ALLOWED_SCHEMES = {"http", "https", "ftp", "ftps"}

DEFAULT_BOX_SIZE = 12
DEFAULT_BORDER = 4


def is_link(value: str) -> bool:
    """Return True if *value* is a URL with an allowed network scheme."""
    parsed = urlparse(value)
    return bool(
        parsed.scheme
        and parsed.netloc
        and parsed.scheme.lower() in ALLOWED_SCHEMES
    )


def safe_filename(link: str) -> str:
    """Build a default filename from the URL's hostname (no credentials)."""
    parsed = urlparse(link)
    # .hostname strips port and user:pass; .netloc does not.
    host = parsed.hostname or ""
    host = re.sub(r"[^a-zA-Z0-9.-]+", "-", host).strip(".-")
    return f"{host or 'link'}-qr.png"


def unique_path(path: Path) -> Path:
    """If *path* already exists, append -1, -2, … until the name is free."""
    if not path.exists():
        return path
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    n = 1
    while True:
        candidate = parent / f"{stem}-{n}{suffix}"
        if not candidate.exists():
            return candidate
        n += 1


def resolve_output(link: str, output: Path | None) -> Path:
    """Decide the final output path, creating parent dirs as needed."""
    downloads = Path.home() / "Downloads"

    if output is None:
        # Default: ~/Downloads/<host>-qr.png
        directory = downloads
        name = safe_filename(link)
    elif output.is_dir() or str(output).endswith(("/", "\\")):
        # User gave a directory, not a file
        directory = output
        name = safe_filename(link)
    else:
        directory = output.parent
        name = output.name
        # Ensure .png without mangling dots (e.g. "my.report.v2" → "my.report.v2.png")
        if not name.lower().endswith(".png"):
            name = name + ".png"

    directory.mkdir(parents=True, exist_ok=True)
    return unique_path(directory / name)


def create_qr(link: str, output: Path) -> Path:
    """Generate a static QR-code PNG for *link* and save it to *output*.

    Raises DataOverflowError if the link is too long for any QR version.
    """
    qr = qrcode.QRCode(
        version=None,
        error_correction=ERROR_CORRECT_H,
        box_size=DEFAULT_BOX_SIZE,
        border=DEFAULT_BORDER,
    )
    qr.add_data(link)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    output.parent.mkdir(parents=True, exist_ok=True)
    img.save(output)
    return output
