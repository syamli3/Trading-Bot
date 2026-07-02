"""
Input validation utilities for the trading bot CLI.

Keeping validation separate from CLI/business logic makes it easy to
unit test and reuse.
"""

import re

VALID_SIDES = {"BUY", "SELL"}
VALID_ORDER_TYPES = {"MARKET", "LIMIT"}

# Basic pattern: 2-10 uppercase letters (e.g., BTCUSDT, ETHUSDT)
SYMBOL_PATTERN = re.compile(r"^[A-Z0-9]{5,15}$")


class ValidationError(Exception):
    """Raised when user-supplied CLI input fails validation."""
    pass


def validate_symbol(symbol: str) -> str:
    symbol = symbol.strip().upper()
    if not SYMBOL_PATTERN.match(symbol):
        raise ValidationError(
            f"Invalid symbol '{symbol}'. Expected format like 'BTCUSDT'."
        )
    return symbol


def validate_side(side: str) -> str:
    side = side.strip().upper()
    if side not in VALID_SIDES:
        raise ValidationError(f"Invalid side '{side}'. Must be one of {VALID_SIDES}.")
    return side


def validate_order_type(order_type: str) -> str:
    order_type = order_type.strip().upper()
    if order_type not in VALID_ORDER_TYPES:
        raise ValidationError(
            f"Invalid order type '{order_type}'. Must be one of {VALID_ORDER_TYPES}."
        )
    return order_type


def validate_quantity(quantity: float) -> float:
    if quantity is None:
        raise ValidationError("Quantity is required.")
    try:
        quantity = float(quantity)
    except (TypeError, ValueError):
        raise ValidationError(f"Quantity must be a number, got '{quantity}'.")
    if quantity <= 0:
        raise ValidationError("Quantity must be greater than zero.")
    return quantity


def validate_price(price: float, order_type: str) -> float:
    """Price is required only for LIMIT orders."""
    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        try:
            price = float(price)
        except (TypeError, ValueError):
            raise ValidationError(f"Price must be a number, got '{price}'.")
        if price <= 0:
            raise ValidationError("Price must be greater than zero.")
        return price
    return None


def validate_order_input(symbol: str, side: str, order_type: str,
                          quantity: float, price: float = None) -> dict:
    """Runs all validations together and returns a clean, normalized dict."""
    clean_symbol = validate_symbol(symbol)
    clean_side = validate_side(side)
    clean_order_type = validate_order_type(order_type)
    clean_quantity = validate_quantity(quantity)
    clean_price = validate_price(price, clean_order_type)

    return {
        "symbol": clean_symbol,
        "side": clean_side,
        "order_type": clean_order_type,
        "quantity": clean_quantity,
        "price": clean_price,
    }
