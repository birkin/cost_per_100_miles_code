#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# ///

import logging
from decimal import Decimal

from lib.calculate_cents_per_kwh import get_ev_100_mile_cost_values, get_gas_100_mile_cost_values, get_rounded_cents_per_kwh


def main() -> None:
    """
    Prints per-entry and overall cents-per-kilowatt-hour values.

    Called by: __main__
    """
    logging.basicConfig(level=logging.DEBUG, format='%(message)s')
    rhode_island_cents_per_kwh = get_rounded_cents_per_kwh()
    ev_100_mile_cost_values: list[tuple[str, Decimal]] = get_ev_100_mile_cost_values(rhode_island_cents_per_kwh)
    gas_100_mile_cost_values: list[tuple[Decimal, list[tuple[Decimal, Decimal]]]] = get_gas_100_mile_cost_values()

    for efficiency_label, cost_per_100_miles in ev_100_mile_cost_values:
        dollars_per_100_miles = cost_per_100_miles / Decimal('100')
        logging.debug('%s: $%.2f per 100 miles', efficiency_label, dollars_per_100_miles)

    for miles_per_gallon, price_cost_values in gas_100_mile_cost_values:
        logging.debug('%s miles/gallon', miles_per_gallon)

        for price_per_gallon, cost_per_100_miles in price_cost_values:
            logging.debug('  $%.2f per gallon: $%.2f per 100 miles', price_per_gallon, cost_per_100_miles)


if __name__ == '__main__':
    main()
