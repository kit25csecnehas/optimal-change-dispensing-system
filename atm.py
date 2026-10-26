
from algorithms import greedy_change, dp_change, number_of_coins


class ATM:
    def __init__(self, denominations, inventory):
        self.denominations = sorted(denominations, reverse=True)
        self.inventory = inventory.copy()
        self.successful_withdrawals = 0
        self.failed_withdrawals = 0
        self.total_dispensed = 0

    def display_inventory(self):
        print("\n--- ATM NOTE INVENTORY ---")
        for note in self.denominations:
            print(f"Rs. {note}: {self.inventory.get(note, 0)} notes")

        total = sum(
            note * self.inventory.get(note, 0)
            for note in self.denominations
        )
        print(f"Total cash available: Rs. {total}")

    def withdraw(self, amount, method="auto"):
        if amount <= 0:
            print("Invalid amount. Enter an amount greater than zero.")
            self.failed_withdrawals += 1
            return False

        if method not in ("auto", "greedy", "dp"):
            print("Invalid method. Choose auto, greedy, or dp.")
            return False

        # Find a valid combination without modifying inventory.
        if method == "greedy":
            solution = greedy_change(amount, self.denominations)
            if solution is None:
                print("Greedy cannot represent this amount.")
                self.failed_withdrawals += 1
                return False

            if any(
                count > self.inventory.get(note, 0)
                for note, count in solution.items()
            ):
                print("Greedy solution exceeds available inventory.")
                self.failed_withdrawals += 1
                return False

        elif method == "dp":
            solution = dp_change(amount, self.denominations)
            if solution is None:
                print("Amount cannot be represented.")
                self.failed_withdrawals += 1
                return False

            if any(
                count > self.inventory.get(note, 0)
                for note, count in solution.items()
            ):
                print("DP solution exceeds available inventory.")
                self.failed_withdrawals += 1
                return False

        else:
            # Bounded DP: inventory limits how many of each note can be used.
            solution = self._bounded_dp(amount)

            if solution is None:
                print("Insufficient inventory or exact change unavailable.")
                self.failed_withdrawals += 1
                return False

        # Update inventory only after a complete solution is found.
        for note, count in solution.items():
            self.inventory[note] -= count

        self.successful_withdrawals += 1
        self.total_dispensed += amount

        print(f"\nWithdrawal successful: Rs. {amount}")
        print("Notes dispensed:", solution)
        print("Total notes:", number_of_coins(solution))
        return True

    def _bounded_dp(self, amount):
        # dp[value] stores the best note combination for that value.
        # Each combination respects the available inventory.
        dp = [None] * (amount + 1)
        dp[0] = {}

        for note in self.denominations:
            available = self.inventory.get(note, 0)

            for _ in range(available):
                for value in range(amount, note - 1, -1):
                    previous = dp[value - note]

                    if previous is None:
                        continue

                    candidate = previous.copy()
                    candidate[note] = candidate.get(note, 0) + 1

                    current = dp[value]

                    if current is None or sum(candidate.values()) < sum(current.values()):
                        dp[value] = candidate

        return dp[amount]

    def display_report(self):
        total = (
            self.successful_withdrawals
            + self.failed_withdrawals
        )

        print("\n--- ATM TRANSACTION REPORT ---")
        print("Total attempted withdrawals:", total)
        print("Successful withdrawals:", self.successful_withdrawals)
        print("Failed withdrawals:", self.failed_withdrawals)
        print("Total cash dispensed: Rs.", self.total_dispensed)

        if total:
            efficiency = self.successful_withdrawals / total * 100
            print(f"Transaction success rate: {efficiency:.2f}%")
