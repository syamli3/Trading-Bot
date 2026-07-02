"""
Order placement logic — sits between the CLI and the Binance client.

Responsible for: calling the client, formatting a clean summary for the
user, and translating API errors into user-friendly messages.
"""

import logging
from binance.exceptions import BinanceAPIException, BinanceOrderException

logger = logging.getLogger("trading_bot")


def print_order_summary(order_input: dict) -> None:
    """Prints the order request summary before sending it."""
    print("\n--- Order Request Summary ---")
    print(f"Symbol     : {order_input['symbol']}")
    print(f"Side       : {order_input['side']}")
    print(f"Order Type : {order_input['order_type']}")
    print(f"Quantity   : {order_input['quantity']}")
    if order_input["order_type"] == "LIMIT":
        print(f"Price      : {order_input['price']}")
    print("------------------------------\n")


def print_order_response(response: dict) -> None:
    """Prints key fields from Binance's order response."""
    print("--- Order Response ---")
    print(f"Order ID     : {response.get('orderId')}")
    print(f"Status       : {response.get('status')}")
    print(f"Executed Qty : {response.get('executedQty')}")
    avg_price = response.get("avgPrice")
    if avg_price is not None:
        print(f"Avg Price    : {avg_price}")
    print("----------------------\n")


def place_order(client_wrapper, order_input: dict) -> bool:
    """
    Orchestrates placing an order:
    1. Print request summary
    2. Call the Binance client
    3. Print response / success or failure message

    Returns True on success, False on failure.
    """
    print_order_summary(order_input)

    try:
        response = client_wrapper.place_order(
            symbol=order_input["symbol"],
            side=order_input["side"],
            order_type=order_input["order_type"],
            quantity=order_input["quantity"],
            price=order_input.get("price"),
        )
        print_order_response(response)
        print("✅ Order placed successfully.")
        return True

    except (BinanceAPIException, BinanceOrderException) as e:
        logger.error(f"Order failed (Binance error): {e}")
        print(f"❌ Order failed: Binance API error — {e}")
        return False

    except Exception as e:
        logger.error(f"Order failed (unexpected error): {e}")
        print(f"❌ Order failed: {e}")
        return False
