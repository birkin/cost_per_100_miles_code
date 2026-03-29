#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# ///

import json
import pathlib
from decimal import Decimal


def load_gas_efficiencies(filepath: pathlib.Path) -> list[Decimal]:
    """
    Loads gas efficiency values from JSON.

    Called by: get_gas_100_mile_cost_values()
    """
    with filepath.open('r', encoding='utf-8') as file_handle:
        efficiencies: list[Decimal] = json.load(file_handle, parse_float=Decimal)
    return efficiencies


def load_gas_prices(filepath: pathlib.Path) -> list[Decimal]:
    """
    Loads gas prices from JSON.

    Called by: get_gas_100_mile_cost_values()
    """
    with filepath.open('r', encoding='utf-8') as file_handle:
        prices: list[Decimal] = json.load(file_handle, parse_float=Decimal)
    return prices


def calculate_gallons_required(distance_miles: Decimal, miles_per_gallon: Decimal) -> Decimal:
    """
    Calculates the gallons required for a given distance and fuel efficiency.

    Called by: calculate_gas_100_mile_cost_values()
    """
    gallons_required: Decimal = distance_miles / miles_per_gallon
    return gallons_required


def calculate_gas_100_mile_cost_values(
    efficiencies: list[Decimal],
    prices: list[Decimal],
) -> list[tuple[Decimal, list[tuple[Decimal, Decimal]]]]:
    """
    Calculates gas cost values for driving 100 miles at each efficiency and price.

    Called by: get_gas_100_mile_cost_values()
    """
    grouped_cost_values: list[tuple[Decimal, list[tuple[Decimal, Decimal]]]] = []

    for efficiency in efficiencies:
        efficiency_values: list[tuple[Decimal, Decimal]] = []

        for price in prices:
            cost_per_100_miles = calculate_gallons_required(Decimal('100'), efficiency) * price
            efficiency_values.append((price, cost_per_100_miles))

        grouped_cost_values.append((efficiency, efficiency_values))

    return grouped_cost_values


def get_gas_100_mile_cost_values() -> list[tuple[Decimal, list[tuple[Decimal, Decimal]]]]:
    """
    Returns gas 100-mile cost values for the configured efficiencies and prices.

    Called by: main()
    """
    module_directory = pathlib.Path(__file__).resolve().parent
    efficiencies_filepath = module_directory / 'gas_efficiency.json'
    prices_filepath = module_directory / 'gas_prices.json'
    efficiencies = load_gas_efficiencies(efficiencies_filepath)
    prices = load_gas_prices(prices_filepath)
    cost_values = calculate_gas_100_mile_cost_values(efficiencies, prices)
    return cost_values
