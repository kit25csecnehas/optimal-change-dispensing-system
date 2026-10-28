
from flask import Flask, render_template, request

app = Flask(__name__)


def greedy_change(amount, denominations):
    result = []
    remaining = amount

    for coin in sorted(denominations, reverse=True):
        count = remaining // coin
        if count:
            result.append((coin, count))
            remaining %= coin

    return result if remaining == 0 else None


def dp_change(amount, denominations):
    infinity = amount + 1
    dp = [infinity] * (amount + 1)
    previous = [0] * (amount + 1)
    dp[0] = 0

    for value in range(1, amount + 1):
        for coin in denominations:
            if coin <= value and dp[value - coin] + 1 < dp[value]:
                dp[value] = dp[value - coin] + 1
                previous[value] = coin

    if dp[amount] == infinity:
        return None

    counts = {}
    remaining = amount

    while remaining > 0:
        coin = previous[remaining]
        counts[coin] = counts.get(coin, 0) + 1
        remaining -= coin

    return sorted(counts.items(), reverse=True)


def format_result(result):
    if result is None:
        return "Cannot dispense this amount with these denominations."
    if not result:
        return "₹0 — no notes required."

    details = ", ".join(
        f"₹{coin} × {count}" for coin, count in result
    )
    total_notes = sum(count for _, count in result)
    return f"{details} | Total notes: {total_notes}"


@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    amount = 6
    denomination_text = "1, 3, 4"
    error = None

    if request.method == "POST":
        try:
            amount = int(request.form.get("amount", "6"))
            denomination_text = request.form.get(
                "denominations", "1, 3, 4"
            )

            denominations = sorted(set(
                int(value.strip())
                for value in denomination_text.split(",")
            ))

            if amount < 0 or amount > 100000:
                raise ValueError("Enter an amount from 0 to 100000.")

            if not denominations or any(
                coin <= 0 for coin in denominations
            ):
                raise ValueError("Denominations must be positive integers.")

            greedy = greedy_change(amount, denominations)
            optimal = dp_change(amount, denominations)

            result = {
                "greedy": format_result(greedy),
                "dp": format_result(optimal),
                "greedy_count": (
                    sum(count for _, count in greedy)
                    if greedy is not None else None
                ),
                "dp_count": (
                    sum(count for _, count in optimal)
                    if optimal is not None else None
                ),
                "amount": amount,
            }

        except (ValueError, TypeError):
            error = "Please enter a valid amount and positive denominations."

    return render_template(
        "index.html",
        result=result,
        amount=amount,
        denomination_text=denomination_text,
        error=error,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
