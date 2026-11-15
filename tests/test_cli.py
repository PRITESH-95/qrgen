"""Tests for qr_generator.cli."""

from pathlib import Path

from qr_generator.cli import main


class TestCLI:
    def test_bad_link_returns_2(self):
        assert main(["not-a-url"]) == 2

    def test_generates_qr(self, tmp_path: Path):
        out = tmp_path / "test.png"
        code = main(["https://example.com", "-o", str(out)])
        assert code == 0
        assert out.exists()
        assert out.stat().st_size > 0

    def test_version(self, capsys):
        try:
            main(["--version"])
        except SystemExit:
            pass
        assert "qrgen" in capsys.readouterr().out
