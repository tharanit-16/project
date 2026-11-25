def evaluate_trade(trade, portfolio):

    quantity = float(trade["quantity"])
    price = float(trade["price"])
    action = trade["action"]
    security_id = trade["security_id"]

    # STEP 1
    if quantity <= 0 or price <= 0:
        return (
            "Rejected",
            "Invalid trade data."
        )

    if action not in ["Buy", "Sell"]:
        return (
            "Rejected",
            "Invalid trade data."
        )

    # STEP 2
    if security_id in portfolio["restricted_securities"]:
        return (
            "Rejected",
            "Security is restricted for this portfolio."
        )

    holdings = portfolio["current_holdings"]

    existing_quantity = 0

    for holding in holdings:

        if holding["security_id"] == security_id:

            existing_quantity = holding["quantity"]
            break

    # STEP 3
    if action == "Sell":

        if existing_quantity < quantity:

            return (
                "Rejected",
                "Insufficient holdings to sell."
            )

    # STEP 4
    if action == "Buy":

        trade_cost = quantity * price

        if trade_cost > portfolio["cash_balance"]:

            return (
                "Rejected",
                "Insufficient cash for this buy order."
            )

    # STEP 5
    if action == "Buy":

        trade_cost = quantity * price

        post_trade_cash = (
            portfolio["cash_balance"]
            - trade_cost
        )

        post_trade_quantity = (
            existing_quantity
            + quantity
        )

        post_trade_security_value = (
            post_trade_quantity
            * price
        )

        other_holdings_value = 0

        for holding in holdings:

            if holding["security_id"] != security_id:

                other_holdings_value += (
                    holding["quantity"]
                    * holding["market_price"]
                )

        total_portfolio_value_after = (
            post_trade_cash
            + post_trade_security_value
            + other_holdings_value
        )

        position_pct = (
            post_trade_security_value
            / total_portfolio_value_after
        )

        if position_pct > portfolio["max_position_pct"]:

            return (
                "Needs Manual Sign-off",
                "Exceeds maximum position concentration — requires approval."
            )

    # STEP 6
    return (
        "Approved",
        "Trade passed all compliance checks."
    )