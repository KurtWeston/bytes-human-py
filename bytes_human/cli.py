"""Command-line interface for bytes-human."""

import sys
import argparse
from bytes_human import to_human, from_human, ByteUnit


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Convert between bytes and human-readable formats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Examples:\n"
               "  bytes-human 1024\n"
               "  bytes-human --from '1.5 GB'\n"
               "  echo 2048 | bytes-human\n"
    )
    
    parser.add_argument(
        "value",
        nargs="?",
        help="Value to convert (bytes or human-readable string)"
    )
    parser.add_argument(
        "--from", "-f",
        dest="from_human_flag",
        action="store_true",
        help="Convert from human-readable to bytes"
    )
    parser.add_argument(
        "--decimal", "-d",
        action="store_true",
        help="Use decimal units (KB, MB, GB) instead of binary (KiB, MiB, GiB)"
    )
    parser.add_argument(
        "--precision", "-p",
        type=int,
        default=1,
        help="Decimal places (0-10, default: 1)"
    )
    parser.add_argument(
        "--rounding", "-r",
        choices=["round", "floor", "ceil"],
        default="round",
        help="Rounding mode (default: round)"
    )
    parser.add_argument(
        "--locale", "-l",
        action="store_true",
        help="Use locale-aware formatting with thousands separators"
    )
    parser.add_argument(
        "--no-space",
        action="store_true",
        help="No space between number and unit"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Strict parsing mode (reject ambiguous units)"
    )
    
    args = parser.parse_args()
    
    value = args.value
    if not value:
        if not sys.stdin.isatty():
            value = sys.stdin.read().strip()
        else:
            parser.print_help()
            sys.exit(1)
    
    unit_system = ByteUnit.DECIMAL if args.decimal else ByteUnit.BINARY
    separator = "" if args.no_space else " "
    
    try:
        if args.from_human_flag:
            result = from_human(value, unit_system=unit_system, strict=args.strict)
            print(result)
        else:
            bytes_value = int(value)
            result = to_human(
                bytes_value,
                unit_system=unit_system,
                precision=args.precision,
                rounding=args.rounding,
                locale_format=args.locale,
                separator=separator
            )
            print(result)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
