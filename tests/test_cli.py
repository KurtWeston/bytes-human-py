"""Tests for bytes_human.cli module."""

import pytest
import sys
from io import StringIO
from unittest.mock import patch
from bytes_human.cli import main


class TestCLI:
    """Tests for CLI functionality."""

    def test_basic_conversion(self, capsys):
        with patch.object(sys, 'argv', ['bytes-human', '1024']):
            main()
        captured = capsys.readouterr()
        assert "1.0 KiB" in captured.out

    def test_from_human_flag(self, capsys):
        with patch.object(sys, 'argv', ['bytes-human', '--from', '1.5 GB']):
            main()
        captured = capsys.readouterr()
        assert "1500000000" in captured.out or "1610612736" in captured.out

    def test_decimal_units(self, capsys):
        with patch.object(sys, 'argv', ['bytes-human', '1000', '--decimal']):
            main()
        captured = capsys.readouterr()
        assert "1.0 KB" in captured.out

    def test_precision_option(self, capsys):
        with patch.object(sys, 'argv', ['bytes-human', '1536', '--precision', '2']):
            main()
        captured = capsys.readouterr()
        assert "1.50" in captured.out

    def test_rounding_modes(self, capsys):
        with patch.object(sys, 'argv', ['bytes-human', '1590', '--rounding', 'ceil']):
            main()
        captured = capsys.readouterr()
        assert "1.6" in captured.out or "2.0" in captured.out

    def test_no_space_separator(self, capsys):
        with patch.object(sys, 'argv', ['bytes-human', '1024', '--no-space']):
            main()
        captured = capsys.readouterr()
        assert "1.0KiB" in captured.out

    def test_stdin_input(self, capsys, monkeypatch):
        monkeypatch.setattr('sys.stdin', StringIO('2048'))
        with patch.object(sys, 'argv', ['bytes-human']):
            with patch.object(sys.stdin, 'isatty', return_value=False):
                main()
        captured = capsys.readouterr()
        assert "2.0 KiB" in captured.out

    def test_invalid_input_error(self, capsys):
        with patch.object(sys, 'argv', ['bytes-human', 'invalid']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error" in captured.err

    def test_no_input_shows_help(self, capsys):
        with patch.object(sys, 'argv', ['bytes-human']):
            with patch.object(sys.stdin, 'isatty', return_value=True):
                with pytest.raises(SystemExit) as exc_info:
                    main()
                assert exc_info.value.code == 1

    def test_strict_mode(self, capsys):
        with patch.object(sys, 'argv', ['bytes-human', '--from', '1 KB', '--strict']):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 1
        captured = capsys.readouterr()
        assert "Error" in captured.err
