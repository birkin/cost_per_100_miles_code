#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# ///

import json
import pathlib
from decimal import ROUND_HALF_UP, Decimal


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


def print_cents_per_kwh_values() -> None:
    """
    Loads the electricity-cost JSON, calculates cents-per-kilowatt-hour values, and prints them.

    Called by: main()
    """
    module_directory = pathlib.Path(__file__).resolve().parent
    filepath = module_directory / 'electricity_cost.json'
    entries = load_entries(filepath)
    per_entry_values, overall_cents_per_kwh, rounded_overall_cents_per_kwh = calculate_aggregate_values(entries)

    for date_key, cents_per_kwh in per_entry_values:
        print(f'{date_key}: {cents_per_kwh} cents/kWh')

    print(f'overall detailed: {overall_cents_per_kwh} cents/kWh')
    print(f'overall rounded: {rounded_overall_cents_per_kwh} cents/kWh')


def get_rounded_cents_per_kwh() -> Decimal:
    """
    Returns the rounded overall cents-per-kilowatt-hour value.

    Called by: main()
    """
    module_directory = pathlib.Path(__file__).resolve().parent
    filepath = module_directory / 'electricity_cost.json'
    entries = load_entries(filepath)
    _, _, rounded_overall_cents_per_kwh = calculate_aggregate_values(entries)
    return rounded_overall_cents_per_kwh


def load_efficiencies(filepath: pathlib.Path) -> list[Decimal]:
    """
    Loads EV efficiency values from JSON.

    Called by: calculate_ev_100_mile_cost_values()
    """
    with filepath.open('r', encoding='utf-8') as file_handle:
        efficiencies: list[Decimal] = json.load(file_handle, parse_float=Decimal)
    return efficiencies


def calculate_ev_100_mile_cost_values(
    efficiencies: list[Decimal],
    cents_per_kwh: Decimal,
) -> list[tuple[Decimal, Decimal]]:
    """
    Calculates EV cost values for driving 100 miles at each efficiency.

    Called by: print_ev_100_mile_cost_values()
    """
    cost_values: list[tuple[Decimal, Decimal]] = []

    for efficiency in efficiencies:
        cost_per_100_miles = (Decimal('100') / efficiency) * cents_per_kwh
        cost_values.append((efficiency, cost_per_100_miles))

    return cost_values


def print_ev_100_mile_cost_values(cents_per_kwh: Decimal) -> None:
    """
    Loads EV efficiencies and prints the cost to drive 100 miles for each value.

    Called by: main()
    """
    module_directory = pathlib.Path(__file__).resolve().parent
    efficiencies_filepath = module_directory / 'ev_efficiency.json'
    efficiencies = load_efficiencies(efficiencies_filepath)
    cost_values = calculate_ev_100_mile_cost_values(efficiencies, cents_per_kwh)

    for efficiency, cost_per_100_miles in cost_values:
        print(f'{efficiency} miles/kWh: {cost_per_100_miles} cents per 100 miles')


def main() -> None:
    """
    Prints per-entry and overall cents-per-kilowatt-hour values.

    Called by: __main__
    """
    print_ev_100_mile_cost_values()


if __name__ == '__main__':
    main()
