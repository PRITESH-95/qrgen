# Permanent Link QR Generator

Generate a **static QR-code PNG** from any link.  
The link is baked directly into the image — no redirect servers, no subscriptions, no expiry.

## Install

With [pipx](https://pipx.pypa.io/) (recommended):

```sh
pipx install git+https://github.com/PRITESH-95/qrgen.git
```

Or with pip:

```sh
pip install git+https://github.com/PRITESH-95/qrgen.git
```

## Usage

```sh
qrgen https://example.com
```

The QR-code PNG is saved to your **Downloads** folder by default (`~/Downloads/<domain>-qr.png`).

To pick a specific output path:

```sh
qrgen https://example.com -o my-code.png
```

If the file already exists a numbered suffix (`-1`, `-2`, …) is added automatically.

## Dev setup

```sh
git clone https://github.com/PRITESH-95/qrgen.git
cd qrgen
python -m venv .venv
# Windows
.\.venv\Scripts\Activate.ps1
# macOS / Linux
# source .venv/bin/activate
pip install -e ".[dev]"
```

### Run tests

```sh
pytest
```

## License

[MIT](LICENSE)
