
import random
from atm import ATM


def run_simulation(number_of_transactions=100, seed=42):
    random.seed(seed)

    # Shared ATM inventory for all transactions.
    atm = ATM(
        denominations=[500, 200, 100, 50, 20, 10],
        inventory={
            500: 100,
            200: 100,
            100: 200,
            50: 200,
            20: 200,
            10: 200,
        },
    )

    amounts = [
        random.randint(1, 200) * 10
        for _ in range(number_of_transactions)
    ]

    print("\n--- 100 TRANSACTION SIMULATION ---")

    for index, amount in enumerate(amounts, start=1):
        success = atm.withdraw(amount, method="auto")
        status = "SUCCESS" if success else "FAILED"
        print(f"Transaction {index}: Rs. {amount} - {status}")

    atm.display_report()

    print("\n--- EFFICIENCY SUMMARY ---")
    total = atm.successful_withdrawals + atm.failed_withdrawals

    if total:
        success_rate = atm.successful_withdrawals / total * 100
        failure_rate = atm.failed_withdrawals / total * 100

        print(f"Transactions attempted: {total}")
        print(f"Success rate: {success_rate:.2f}%")
        print(f"Failure rate: {failure_rate:.2f}%")
        print(f"Cash dispensed: Rs. {atm.total_dispensed}")

        if atm.successful_withdrawals:
            average = (
                atm.total_dispensed / atm.successful_withdrawals
            )
            print(f"Average successful withdrawal: Rs. {average:.2f}")

    return atm


if __name__ == "__main__":
    run_simulation()
