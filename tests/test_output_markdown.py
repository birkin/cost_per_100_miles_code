import tempfile
import unittest
from decimal import Decimal
from pathlib import Path

from lib.output_markdown import output_markdown


class TestOutputMarkdown(unittest.TestCase):
    """
    Checks markdown file generation for EV and gas cost values.
    """

    def test_output_markdown_writes_expected_content(self) -> None:
        """
        Checks markdown output with representative EV and gas values.
        """
        ev_100_mile_cost_values: list[tuple[str, Decimal]] = [
            ('2.5 miles/kWh', Decimal('1040')),
        ]
        gas_100_mile_cost_values: list[tuple[Decimal, list[tuple[Decimal, Decimal]]]] = [
            (
                Decimal('20'),
                [
                    (Decimal('3.50'), Decimal('17.50')),
                ],
            ),
        ]

        with tempfile.TemporaryDirectory() as temp_directory:
            output_filepath = Path(temp_directory) / 'ev_vs_gasv_costs.md'
            written_filepath = output_markdown(
                ev_100_mile_cost_values,
                gas_100_mile_cost_values,
                output_filepath,
            )

            self.assertEqual(written_filepath, output_filepath)
            contents = output_filepath.read_text(encoding='utf-8')

        self.assertIn('# EV vs Gas Vehicle Costs', contents)
        self.assertIn('## EV Costs', contents)
        self.assertIn('- 2.5 miles/kWh: $10.40 per 100 miles', contents)
        self.assertIn('## Gas Costs', contents)
        self.assertIn('### 20 miles/gallon', contents)
        self.assertIn('  - $3.50 per gallon: $17.50 per 100 miles', contents)

    def test_output_markdown_handles_empty_values(self) -> None:
        """
        Checks markdown output with empty EV and gas value collections.
        """
        with tempfile.TemporaryDirectory() as temp_directory:
            output_filepath = Path(temp_directory) / 'ev_vs_gasv_costs.md'
            output_markdown([], [], output_filepath)
            contents = output_filepath.read_text(encoding='utf-8')

        self.assertIn('# EV vs Gas Vehicle Costs', contents)
        self.assertIn('## EV Costs', contents)
        self.assertIn('## Gas Costs', contents)
        self.assertNotIn('miles/kWh', contents)
        self.assertNotIn('miles/gallon', contents)


if __name__ == '__main__':
    unittest.main()
