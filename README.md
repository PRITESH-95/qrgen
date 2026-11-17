<div align="center">

# qrgen

**Turn any link into a permanent, static QR code PNG.**
The link is baked straight into the image. No redirect servers, no subscriptions, no expiry.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![Interface](https://img.shields.io/badge/Interface-CLI-black)

</div>

---

## Features

- **Static QR codes:** the PNG contains your link itself, so it works forever.
- **One command:** `qrgen <link>` and the image lands in your Downloads folder.
- **Installable CLI:** works with `pipx` or `pip`, no manual setup.
- **Tested:** the `tests/` folder covers the core generator and the CLI.

## Install

With [pipx](https://pipx.pypa.io/) (recommended):

```powershell
pipx install git+https://github.com/PRITESH-95/qrgen.git
```

Or with pip:

```powershell
pip install git+https://github.com/PRITESH-95/qrgen.git
```

## Usage

```powershell
qrgen https://example.com
```

The QR code is saved to your **Downloads** folder as `~/Downloads/<domain>-qr.png`.

See every option, including choosing your own output path:

```powershell
qrgen --help
```

## Project structure

```
qrgen/
+-- src/qr_generator/
|   +-- cli.py          # command-line interface
|   +-- core.py         # QR code generation
|   +-- __main__.py     # python -m qr_generator
+-- tests/
|   +-- test_cli.py
|   +-- test_core.py
+-- pyproject.toml
+-- LICENSE
```

## Development

```powershell
git clone https://github.com/PRITESH-95/qrgen.git
cd qrgen
pip install -e .
pip install pytest
pytest
```

## Built with

Python, [qrcode](https://pypi.org/project/qrcode/) + Pillow, packaged with Hatchling.

## License

MIT. See [LICENSE](LICENSE).
