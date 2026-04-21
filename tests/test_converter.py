"""Tests for bytes_human.converter module."""

import pytest
import math
from bytes_human.converter import to_human, from_human, ByteUnit


class TestToHuman:
    """Tests for to_human function."""

    def test_basic_binary_conversion(self):
        assert to_human(1024) == "1.0 KiB"
        assert to_human(1048576) == "1.0 MiB"
        assert to_human(1073741824) == "1.0 GiB"

    def test_basic_decimal_conversion(self):
        assert to_human(1000, unit_system=ByteUnit.DECIMAL) == "1.0 KB"
        assert to_human(1000000, unit_system=ByteUnit.DECIMAL) == "1.0 MB"
        assert to_human(1000000000, unit_system=ByteUnit.DECIMAL) == "1.0 GB"

    def test_zero_bytes(self):
        assert to_human(0) == "0 B"
        assert to_human(0, unit_system=ByteUnit.DECIMAL) == "0 B"

    def test_negative_values(self):
        assert to_human(-1024) == "-1.0 KiB"
        assert to_human(-1000, unit_system=ByteUnit.DECIMAL) == "-1.0 KB"

    def test_precision_control(self):
        assert to_human(1536, precision=0) == "2 KiB"
        assert to_human(1536, precision=2) == "1.50 KiB"
        assert to_human(1536, precision=3) == "1.500 KiB"

    def test_precision_validation(self):
        with pytest.raises(ValueError, match="Precision must be between 0 and 10"):
            to_human(1024, precision=-1)
        with pytest.raises(ValueError, match="Precision must be between 0 and 10"):
            to_human(1024, precision=11)

    def test_rounding_modes(self):
        assert to_human(1536, precision=1, rounding="round") == "1.5 KiB"
        assert to_human(1536, precision=1, rounding="floor") == "1.5 KiB"
        assert to_human(1590, precision=1, rounding="ceil") == "1.6 KiB"

    def test_locale_formatting(self):
        result = to_human(1234567890, precision=2, locale_format=True)
        assert "1,177.38" in result or "1.177,38" in result

    def test_custom_separator(self):
        assert to_human(1024, separator="") == "1.0KiB"
        assert to_human(1024, separator="-") == "1.0-KiB"

    def test_very_large_numbers(self):
        assert "PiB" in to_human(1024**5)
        assert "PB" in to_human(1000**5, unit_system=ByteUnit.DECIMAL)

    def test_small_values(self):
        assert to_human(1) == "1 B"
        assert to_human(999) == "999 B"


class TestFromHuman:
    """Tests for from_human function."""

    def test_basic_binary_parsing(self):
        assert from_human("1 KiB") == 1024
        assert from_human("1 MiB") == 1048576
        assert from_human("1 GiB") == 1073741824

    def test_basic_decimal_parsing(self):
        assert from_human("1 KB", unit_system=ByteUnit.DECIMAL) == 1000
        assert from_human("1 MB", unit_system=ByteUnit.DECIMAL) == 1000000
        assert from_human("1 GB", unit_system=ByteUnit.DECIMAL) == 1000000000

    def test_auto_detect_units(self):
        assert from_human("1 KiB") == 1024
        assert from_human("1 KB") == 1000

    def test_decimal_values(self):
        assert from_human("1.5 KiB") == 1536
        assert from_human("2.5 MB", unit_system=ByteUnit.DECIMAL) == 2500000

    def test_whitespace_handling(self):
        assert from_human("  1 KiB  ") == 1024
        assert from_human("1KiB") == 1024
        assert from_human("1  KiB") == 1024

    def test_thousands_separator(self):
        assert from_human("1,024 B") == 1024
        assert from_human("1,000 KB") == 1000000

    def test_negative_values(self):
        assert from_human("-1 KiB") == -1024
        assert from_human("-1.5 MB") == -1500000

    def test_case_insensitive(self):
        assert from_human("1 kib") == 1024
        assert from_human("1 KB") == 1000

    def test_strict_mode(self):
        with pytest.raises(ValueError, match="Ambiguous unit"):
            from_human("1 KB", strict=True)
        assert from_human("1 KiB", strict=True) == 1024

    def test_invalid_format(self):
        with pytest.raises(ValueError, match="Invalid format"):
            from_human("invalid")
        with pytest.raises(ValueError, match="Invalid format"):
            from_human("1.2.3 KB")

    def test_unknown_unit(self):
        with pytest.raises(ValueError, match="Unknown unit"):
            from_human("1 XB")

    def test_bytes_only(self):
        assert from_human("1024 B") == 1024
        assert from_human("0 B") == 0
