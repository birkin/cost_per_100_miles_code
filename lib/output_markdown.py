#!/usr/bin/env -S uv run
# /// script
# requires-python = ">=3.12"
# ///

from decimal import Decimal
from pathlib import Path


def format_money(value: Decimal) -> str:
    """
    Formats a decimal value as dollars and cents.

    Called by: build_markdown()
    """
    return f'${value:.2f}'


def build_markdown(
    ev_100_mile_cost_values: list[tuple[str, Decimal]],
    gas_100_mile_cost_values: list[tuple[Decimal, list[tuple[Decimal, Decimal]]]],
) -> str:
    """
    Builds the EV versus gas markdown content.

    Called by: output_markdown()
    """
    lines: list[str] = []

    lines.append('# EV vs Gas Vehicle Costs')
    lines.append('')

    lines.append('## EV Costs')
    lines.append('')

    for efficiency_label, cost_per_100_miles in ev_100_mile_cost_values:
        dollars_per_100_miles = cost_per_100_miles / Decimal('100')
        lines.append(f'- {efficiency_label}: {format_money(dollars_per_100_miles)} per 100 miles')

    lines.append('')
    lines.append('## Gas Costs')
    lines.append('')

    for miles_per_gallon, price_cost_values in gas_100_mile_cost_values:
        lines.append(f'### {miles_per_gallon} miles/gallon')
        lines.append('')

        for price_per_gallon, cost_per_100_miles in price_cost_values:
            lines.append(
                f'  - {format_money(price_per_gallon)} per gallon: '
                f'{format_money(cost_per_100_miles)} per 100 miles'
            )

        lines.append('')

    markdown = '\n'.join(lines).rstrip() + '\n'
    return markdown


def output_markdown(
    ev_100_mile_cost_values: list[tuple[str, Decimal]],
    gas_100_mile_cost_values: list[tuple[Decimal, list[tuple[Decimal, Decimal]]]],
    output_filepath: Path | None = None,
) -> Path:
    """
    Builds the markdown content and saves it to disk.

    Called by: main()
    """
    module_directory = Path(__file__).resolve().parent
    project_directory = module_directory.parent
    target_filepath = output_filepath if output_filepath is not None else project_directory / 'ev_vs_gasv_costs.md'
    markdown = build_markdown(ev_100_mile_cost_values, gas_100_mile_cost_values)
    target_filepath.parent.mkdir(parents=True, exist_ok=True)
    target_filepath.write_text(markdown, encoding='utf-8')
    return target_filepath
