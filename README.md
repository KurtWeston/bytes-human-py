# bytes-human

Convert between byte sizes and human-readable formats with locale-aware formatting and precision control

## Features

- Convert bytes to human-readable format (e.g., 1024 → '1.0 KB' or '1.0 KiB')
- Parse human-readable sizes back to bytes (e.g., '1.5 GB' → 1610612736)
- Support both binary units (KiB, MiB, GiB, TiB, PiB) and decimal units (KB, MB, GB, TB, PB)
- Configurable precision for decimal places (0-10)
- Configurable rounding modes (round, floor, ceil)
- Locale-aware number formatting with thousands separators
- Handle edge cases: zero bytes, negative values, very large numbers
- CLI mode for interactive conversions and shell scripting
- Library mode for programmatic usage in Python applications
- Pipe support for processing output from other commands
- Auto-detect optimal unit for readability
- Strict parsing mode to reject ambiguous inputs
- Custom unit separator configuration (space, no-space)

## How to Use

Use this project when you need to:

- Quickly solve problems related to bytes-human
- Integrate python functionality into your workflow
- Learn how python handles common patterns

## Installation

```bash
# Clone the repository
git clone https://github.com/KurtWeston/bytes-human.git
cd bytes-human

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
python main.py
```

## Built With

- python

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
