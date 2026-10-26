
from atm import ATM
from algorithms import greedy_change, dp_change, number_of_coins


def compare_algorithms():
    denominations = [1, 3, 4]
    amount = 6

    greedy = greedy_change(amount, denominations)
    optimal = dp_change(amount, denominations)

    print("\n--- GREEDY vs DYNAMIC PROGRAMMING ---")
    print("Amount: Rs.", amount)
    print("Denominations:", denominations)
    print("Greedy:", greedy, "| Notes:", number_of_coins(greedy))
    print("DP:", optimal, "| Notes:", number_of_coins(optimal))


def main():
    atm = ATM(
        denominations=[500, 200, 100, 50, 20, 10, 1, 3, 4],
        inventory={
            500: 10,
            200: 10,
            100: 20,
            50: 20,
            20: 20,
            10: 20,
            4: 10,
            3: 10,
            1: 50,
        },
    )

    while True:
        print("\n========== OPTIMAL CHANGE DISPENSING SYSTEM ==========")
        print("1. Withdraw cash (automatic optimal change)")
        print("2. Display note inventory")
        print("3. Compare Greedy and DP")
        print("4. Display transaction report")
        print("5. Run 100-transaction simulation")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            try:
                amount = int(input("Enter withdrawal amount: "))
            except ValueError:
                print("Please enter a whole number.")
                continue

            atm.withdraw(amount, method="auto")

        elif choice == "2":
            atm.display_inventory()

        elif choice == "3":
            compare_algorithms()

        elif choice == "4":
            atm.display_report()

        elif choice == "5":
            from simulation import run_simulation
            run_simulation(100)

        elif choice == "6":
            print("Thank you for using the simulator!")
            break

        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()
