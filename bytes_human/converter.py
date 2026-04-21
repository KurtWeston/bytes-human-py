"""Core conversion logic for bytes to human-readable formats."""

import re
import math
from enum import Enum
from typing import Optional, Literal


class ByteUnit(Enum):
    """Byte unit systems."""
    BINARY = "binary"
    DECIMAL = "decimal"


BINARY_UNITS = [("PiB", 1024**5), ("TiB", 1024**4), ("GiB", 1024**3),
                ("MiB", 1024**2), ("KiB", 1024), ("B", 1)]

DECIMAL_UNITS = [("PB", 1000**5), ("TB", 1000**4), ("GB", 1000**3),
                 ("MB", 1000**2), ("KB", 1000), ("B", 1)]


def to_human(
    bytes_value: int,
    unit_system: ByteUnit = ByteUnit.BINARY,
    precision: int = 1,
    rounding: Literal["round", "floor", "ceil"] = "round",
    locale_format: bool = False,
    separator: str = " "
) -> str:
    """Convert bytes to human-readable format.
    
    Args:
        bytes_value: Number of bytes to convert
        unit_system: Binary (1024) or decimal (1000) units
        precision: Decimal places (0-10)
        rounding: Rounding mode
        locale_format: Use locale-aware number formatting
        separator: String between number and unit
    
    Returns:
        Human-readable string (e.g., "1.5 GiB")
    
    Raises:
        ValueError: If precision is out of range
    """
    if not 0 <= precision <= 10:
        raise ValueError("Precision must be between 0 and 10")
    
    if bytes_value == 0:
        return f"0{separator}B"
    
    is_negative = bytes_value < 0
    abs_bytes = abs(bytes_value)
    
    units = BINARY_UNITS if unit_system == ByteUnit.BINARY else DECIMAL_UNITS
    
    for unit_name, unit_size in units:
        if abs_bytes >= unit_size:
            value = abs_bytes / unit_size
            
            if rounding == "floor":
                value = math.floor(value * (10 ** precision)) / (10 ** precision)
            elif rounding == "ceil":
                value = math.ceil(value * (10 ** precision)) / (10 ** precision)
            else:
                value = round(value, precision)
            
            if is_negative:
                value = -value
            
            if locale_format:
                formatted = f"{value:,.{precision}f}"
            else:
                formatted = f"{value:.{precision}f}"
            
            return f"{formatted}{separator}{unit_name}"
    
    return f"{bytes_value}{separator}B"


def from_human(
    human_str: str,
    unit_system: Optional[ByteUnit] = None,
    strict: bool = False
) -> int:
    """Parse human-readable size to bytes.
    
    Args:
        human_str: String like "1.5 GB" or "2 GiB"
        unit_system: Force binary or decimal (auto-detect if None)
        strict: Reject ambiguous inputs (KB without i)
    
    Returns:
        Number of bytes
    
    Raises:
        ValueError: If string format is invalid or ambiguous
    """
    human_str = human_str.strip().replace(",", "")
    
    pattern = r"^([+-]?\d+\.?\d*)\s*([A-Za-z]+)$"
    match = re.match(pattern, human_str)
    
    if not match:
        raise ValueError(f"Invalid format: {human_str}")
    
    value_str, unit = match.groups()
    value = float(value_str)
    unit = unit.upper()
    
    if unit == "B":
        return int(value)
    
    is_binary = "I" in unit
    unit_base = unit.replace("I", "")
    
    if strict and not is_binary and unit != "B":
        raise ValueError(f"Ambiguous unit '{unit}' in strict mode. Use 'iB' suffix for binary.")
    
    if unit_system:
        use_binary = unit_system == ByteUnit.BINARY
    else:
        use_binary = is_binary
    
    units_map = {
        "KB": 1024 if use_binary else 1000,
        "MB": 1024**2 if use_binary else 1000**2,
        "GB": 1024**3 if use_binary else 1000**3,
        "TB": 1024**4 if use_binary else 1000**4,
        "PB": 1024**5 if use_binary else 1000**5,
    }
    
    if unit_base not in units_map:
        raise ValueError(f"Unknown unit: {unit}")
    
    return int(value * units_map[unit_base])
