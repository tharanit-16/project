import csv
import json

from compliance_engine import evaluate_trade


def load_portfolios():

    with open("portfolios.json", "r") as file:
        return json.load(file)


def load_trades():

    with open("trades_test.csv", "r") as file:
        return list(csv.DictReader(file))


def process_trades(portfolios, trades):

    results = []

    for trade in trades:

        portfolio_id = trade["portfolio_id"]

        if portfolio_id not in portfolios:

            results.append({
                "portfolio_id": portfolio_id,
                "security_id": trade["security_id"],
                "action": trade["action"],
                "decision": "Rejected",
                "reason": "Portfolio not found."
            })

            continue

        portfolio = portfolios[portfolio_id]

        decision, reason = evaluate_trade(
            trade,
            portfolio
        )

        results.append({
            "portfolio_id": trade["portfolio_id"],
            "security_id": trade["security_id"],
            "action": trade["action"],
            "quantity": trade["quantity"],
            "price": trade["price"],
            "decision": decision,
            "reason": reason
        })

    return results


def save_results(results):

    with open(
        "output.csv",
        "w",
        newline=""
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "portfolio_id",
                "security_id",
                "action",
                "quantity",
                "price",
                "decision",
                "reason"
            ]
        )

        writer.writeheader()
        writer.writerows(results)


def display_results(results):

    print("\nTRADE COMPLIANCE RESULTS")
    print("-" * 80)

    for result in results:

        print(
            f"{result['portfolio_id']} | "
            f"{result['security_id']} | "
            f"{result['action']} | "
            f"{result['decision']} | "
            f"{result['reason']}"
        )


def main():

    portfolios = load_portfolios()

    trades = load_trades()

    results = process_trades(
        portfolios,
        trades
    )

    display_results(results)

    save_results(results)

    print("\nOutput saved to output.csv")


if __name__ == "__main__":
    main()