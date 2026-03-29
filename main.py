#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# ///

from lib.calculate_cents_per_kwh import get_rounded_cents_per_kwh


def main() -> None:
    """
    Prints per-entry and overall cents-per-kilowatt-hour values.

    Called by: __main__
    """
    rhode_island_cents_per_kwh = get_rounded_cents_per_kwh()
    print(f'Rhode Island cents per kWh: {rhode_island_cents_per_kwh}')


if __name__ == '__main__':
    main()
