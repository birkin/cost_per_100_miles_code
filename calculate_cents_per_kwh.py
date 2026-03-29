#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# ///

from decimal import Decimal, ROUND_HALF_UP
import json
import pathlib


def load_entries(filepath: pathlib.Path) -> list[dict[str, dict[str, Decimal]]]:
    """
    Loads the electricity-cost entries from JSON.

    Called by: main()
    """
    with filepath.open('r', encoding='utf-8') as file_handle:
        entries: list[dict[str, dict[str, Decimal]]] = json.load(file_handle, parse_float=Decimal)
    return entries


def calculate_cents_per_kwh(cost_usd: Decimal, kilowatt_hours: int) -> Decimal:
    """
    Calculates cents per kilowatt hour from a dollar cost and kilowatt-hours value.

    Called by: calculate_aggregate_values()
    """
    cents_per_kwh: Decimal = (cost_usd * Decimal('100')) / Decimal(kilowatt_hours)
    return cents_per_kwh


def round_to_nearest_integer_cent(cents_per_kwh: Decimal) -> Decimal:
    """
    Rounds a cents-per-kilowatt-hour value to the nearest whole cent.

    Called by: calculate_aggregate_values()
    """
    rounded_cents_per_kwh: Decimal = cents_per_kwh.quantize(Decimal('1'), rounding=ROUND_HALF_UP)
    return rounded_cents_per_kwh


def calculate_aggregate_values(
    entries: list[dict[str, dict[str, Decimal]]],
) -> tuple[list[tuple[str, Decimal]], Decimal, Decimal]:
    """
    Calculates per-entry and overall cents-per-kilowatt-hour values.

    Called by: main()
    """
    per_entry_values: list[tuple[str, Decimal]] = []
    total_cost_usd = Decimal('0')
    total_kilowatt_hours = 0

    for entry in entries:
        for date_key, data in entry.items():
            kilowatt_hours = int(data['kilowatt_hours'])
            cost_usd = data['cost_usd']
            cents_per_kwh = calculate_cents_per_kwh(cost_usd, kilowatt_hours)
            per_entry_values.append((date_key, cents_per_kwh))
            total_cost_usd += cost_usd
            total_kilowatt_hours += kilowatt_hours

    overall_cents_per_kwh = calculate_cents_per_kwh(total_cost_usd, total_kilowatt_hours)
    rounded_overall_cents_per_kwh = round_to_nearest_integer_cent(overall_cents_per_kwh)
    result = (per_entry_values, overall_cents_per_kwh, rounded_overall_cents_per_kwh)
    return result


def main() -> None:
    """
    Prints per-entry and overall cents-per-kilowatt-hour values.

    Called by: __main__
    """
    filepath = pathlib.Path('/mnt/data/electricity_cost.json')
    entries = load_entries(filepath)
    per_entry_values, overall_cents_per_kwh, rounded_overall_cents_per_kwh = calculate_aggregate_values(entries)

    for date_key, cents_per_kwh in per_entry_values:
        print(f'{date_key}: {cents_per_kwh} cents/kWh')

    print(f'overall detailed: {overall_cents_per_kwh} cents/kWh')
    print(f'overall rounded: {rounded_overall_cents_per_kwh} cents/kWh')


if __name__ == '__main__':
    main()
