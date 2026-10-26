
def greedy_change(amount, denominations):
    """Use the largest denomination possible at each step."""
    denominations = sorted(denominations, reverse=True)
    result = {}
    remaining = amount

    for coin in denominations:
        count = remaining // coin
        if count > 0:
            result[coin] = count
            remaining %= coin

    if remaining != 0:
        return None

    return result


def dp_change(amount, denominations):
    """Find a minimum-number-of-coins solution using DP."""
    denominations = sorted(set(denominations))

    # dp[x] = minimum number of coins needed for amount x
    dp = [float("inf")] * (amount + 1)
    previous_coin = [None] * (amount + 1)
    dp[0] = 0

    for value in range(1, amount + 1):
        for coin in denominations:
            if coin <= value and dp[value - coin] + 1 < dp[value]:
                dp[value] = dp[value - coin] + 1
                previous_coin[value] = coin

    if dp[amount] == float("inf"):
        return None

    result = {}
    remaining = amount

    while remaining > 0:
        coin = previous_coin[remaining]
        result[coin] = result.get(coin, 0) + 1
        remaining -= coin

    return result


def number_of_coins(solution):
    """Count the total notes or coins in a solution."""
    if solution is None:
        return None
    return sum(solution.values())


if __name__ == "__main__":
    denominations = [1, 3, 4]
    amount = 6

    greedy_result = greedy_change(amount, denominations)
    dp_result = dp_change(amount, denominations)

    print("Amount:", amount)
    print("Denominations:", denominations)
    print("Greedy result:", greedy_result)
    print("Greedy coin count:", number_of_coins(greedy_result))
    print("DP result:", dp_result)
    print("DP coin count:", number_of_coins(dp_result))
