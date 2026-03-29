import unittest
from decimal import Decimal

from lib.calculate_cents_per_kwh import calculate_gallons_required, calculate_gas_100_mile_cost_values


class TestGasCostCalculations(unittest.TestCase):
    """
    Checks gas mileage and 100-mile cost calculations.
    """

    def test_calculate_gallons_required_for_400_miles(self) -> None:
        """
        Checks gallons required for 400 miles at 20 miles per gallon.
        """
        gallons_required = calculate_gallons_required(Decimal('400'), Decimal('20'))

        self.assertEqual(gallons_required, Decimal('20'))

    def test_calculate_gas_100_mile_cost_values(self) -> None:
        """
        Checks 100-mile gas cost values for one MPG and one gasoline price.
        """
        cost_values = calculate_gas_100_mile_cost_values([Decimal('20')], [Decimal('3.50')])

        self.assertEqual(cost_values, [(Decimal('20'), [(Decimal('3.50'), Decimal('17.5'))])])


if __name__ == '__main__':
    unittest.main()
