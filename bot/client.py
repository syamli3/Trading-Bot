"""
Binance Futures Testnet client wrapper.

This module isolates all direct interaction with the Binance API so the
rest of the app (CLI, order logic) doesn't need to know API details.
Uses the python-binance library, pointed at the Futures Testnet endpoint.
"""

import logging
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

logger = logging.getLogger("trading_bot")

FUTURES_TESTNET_URL = "https://testnet.binancefuture.com/fapi"


class BinanceFuturesTestnetClient:
    """Thin wrapper around python-binance's Client, locked to Futures Testnet."""

    def __init__(self, api_key: str, api_secret: str):
        if not api_key or not api_secret:
            raise ValueError("API key and secret must be provided.")

        # ping=False: skip python-binance's default spot-API ping on init,
        # since this bot only talks to the Futures Testnet endpoints.
        self.client = Client(api_key, api_secret, ping=False)
        # Redirect the futures endpoints to testnet
        self.client.FUTURES_URL = FUTURES_TESTNET_URL
        logger.debug("Initialized Binance Futures Testnet client.")

    def place_order(self, symbol: str, side: str, order_type: str,
                     quantity: float, price: float = None) -> dict:
        """
        Places a MARKET or LIMIT order on Binance Futures Testnet.

        Returns the raw order response dict from Binance on success.
        Raises BinanceAPIException / BinanceOrderException on failure,
        which the caller (orders.py) is expected to catch and log.
        """
        order_params = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }

        if order_type == "LIMIT":
            # LIMIT orders on Binance Futures require timeInForce
            order_params["price"] = price
            order_params["timeInForce"] = "GTC"  # Good-Til-Cancelled

        logger.info(f"Sending order request: {order_params}")

        try:
            response = self.client.futures_create_order(**order_params)
            logger.info(f"Order response received: {response}")
            return response
        except (BinanceAPIException, BinanceOrderException) as e:
            logger.error(f"Binance API error while placing order: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected/network error while placing order: {e}")
            raise
