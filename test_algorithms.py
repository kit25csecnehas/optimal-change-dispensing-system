
import unittest
from algorithms import greedy_change, dp_change, number_of_coins
from atm import ATM


class TestChangeAlgorithms(unittest.TestCase):

    def test_greedy_failure_case(self):
        result = greedy_change(6, [1, 3, 4])
        self.assertEqual(number_of_coins(result), 3)

    def test_dp_finds_optimal_solution(self):
        result = dp_change(6, [1, 3, 4])
        self.assertEqual(number_of_coins(result), 2)
        self.assertEqual(sum(
            coin * count for coin, count in result.items()
        ), 6)

    def test_standard_denominations(self):
        result = greedy_change(780, [500, 200, 100, 50, 20, 10])
        self.assertEqual(number_of_coins(result), 5)

    def test_unrepresentable_amount(self):
        result = dp_change(5, [2, 4])
        self.assertIsNone(result)

    def test_inventory_is_not_overdrawn(self):
        atm = ATM([500, 100], {500: 1, 100: 0})
        result = atm.withdraw(600)
        self.assertFalse(result)
        self.assertEqual(atm.inventory[500], 1)

    def test_successful_withdrawal_updates_inventory(self):
        atm = ATM([500, 100], {500: 2, 100: 2})
        result = atm.withdraw(500)
        self.assertTrue(result)
        self.assertEqual(atm.inventory[500], 1)
        self.assertEqual(atm.total_dispensed, 500)


if __name__ == "__main__":
    unittest.main()
