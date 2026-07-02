"""
CLI entry point for the trading bot.

Parses command-line arguments, validates them, and delegates order
placement to orders.py / client.py. This file should contain no
direct Binance API calls — only argument handling and wiring.

Usage:
    python -m bot.cli --api-key KEY --api-secret SECRET \
        --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

    python -m bot.cli --api-key KEY --api-secret SECRET \
        --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 60000
"""

import argparse
import os
import sys

from bot.logging_config import setup_logger
from bot.validators import validate_order_input, ValidationError
from bot.client import BinanceFuturesTestnetClient
from bot.orders import place_order

logger = setup_logger()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Simplified trading bot for Binance Futures Testnet (USDT-M)."
    )
    parser.add_argument(
        "--api-key",
        default=os.environ.get("BINANCE_API_KEY"),
        help="Binance Futures Testnet API key (or set BINANCE_API_KEY env var).",
    )
    parser.add_argument(
        "--api-secret",
        default=os.environ.get("BINANCE_API_SECRET"),
        help="Binance Futures Testnet API secret (or set BINANCE_API_SECRET env var).",
    )
    parser.add_argument("--symbol", required=True, help="Trading pair, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, choices=["BUY", "SELL", "buy", "sell"])
    parser.add_argument(
        "--type", dest="order_type", required=True,
        choices=["MARKET", "LIMIT", "market", "limit"],
    )
    parser.add_argument("--quantity", required=True, type=float, help="Order quantity")
    parser.add_argument(
        "--price", required=False, type=float,
        help="Order price (required for LIMIT orders)",
    )
    return parser


def main():
    parser = build_parser()
    args = parser.parse_args()

    if not args.api_key or not args.api_secret:
        print("❌ Error: API key and secret are required "
              "(pass --api-key/--api-secret or set BINANCE_API_KEY/BINANCE_API_SECRET).")
        sys.exit(1)

    try:
        order_input = validate_order_input(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValidationError as e:
        logger.error(f"Input validation failed: {e}")
        print(f"❌ Invalid input: {e}")
        sys.exit(1)

    try:
        client_wrapper = BinanceFuturesTestnetClient(args.api_key, args.api_secret)
    except ValueError as e:
        logger.error(f"Client initialization failed: {e}")
        print(f"❌ {e}")
        sys.exit(1)

    success = place_order(client_wrapper, order_input)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
