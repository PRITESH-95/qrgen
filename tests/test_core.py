"""Tests for qr_generator.core."""

from pathlib import Path

import pytest

from qr_generator.core import is_link, safe_filename, unique_path, resolve_output


# ── is_link ────────────────────────────────────────────────────

class TestIsLink:
    def test_valid_https(self):
        assert is_link("https://example.com") is True

    def test_valid_http(self):
        assert is_link("http://example.com/path?q=1") is True

    def test_ftp(self):
        assert is_link("ftp://files.example.com") is True

    def test_rejects_no_scheme(self):
        assert is_link("example.com") is False

    def test_rejects_javascript_scheme(self):
        assert is_link("javascript:alert(1)") is False

    def test_rejects_data_scheme(self):
        assert is_link("data:text/plain;base64,SGVsbG8=") is False

    def test_rejects_empty(self):
        assert is_link("") is False


# ── safe_filename ──────────────────────────────────────────────

class TestSafeFilename:
    def test_simple_domain(self):
        assert safe_filename("https://example.com") == "example.com-qr.png"

    def test_strips_credentials(self):
        # hostname is used, not netloc — so user:pass never leaks
        name = safe_filename("https://user:pass@secret.io/page")
        assert "user" not in name
        assert "pass" not in name
        assert name == "secret.io-qr.png"

    def test_fallback(self):
        assert safe_filename("https:///path") == "link-qr.png"


# ── unique_path ────────────────────────────────────────────────

class TestUniquePath:
    def test_no_conflict(self, tmp_path: Path):
        p = tmp_path / "file.png"
        assert unique_path(p) == p

    def test_appends_number(self, tmp_path: Path):
        p = tmp_path / "file.png"
        p.touch()
        assert unique_path(p) == tmp_path / "file-1.png"

    def test_increments(self, tmp_path: Path):
        p = tmp_path / "file.png"
        p.touch()
        (tmp_path / "file-1.png").touch()
        assert unique_path(p) == tmp_path / "file-2.png"


# ── resolve_output ─────────────────────────────────────────────

class TestResolveOutput:
    def test_default_goes_to_downloads(self):
        out = resolve_output("https://example.com", None)
        assert "Downloads" in str(out)
        assert out.name == "example.com-qr.png"

    def test_explicit_file(self, tmp_path: Path):
        target = tmp_path / "my-code.png"
        out = resolve_output("https://example.com", target)
        assert out == target

    def test_adds_png_suffix(self, tmp_path: Path):
        target = tmp_path / "my-code"
        out = resolve_output("https://example.com", target)
        assert out.name == "my-code.png"

    def test_directory_uses_default_name(self, tmp_path: Path):
        out = resolve_output("https://example.com", tmp_path)
        assert out.parent == tmp_path
        assert out.name == "example.com-qr.png"
