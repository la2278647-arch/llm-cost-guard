"""Built-in model price table. Prices are USD per 1M tokens.

Keep this table current — pricing pages are the source of truth.
Users may override/extend at runtime via `lcg prices add`.
"""

# model_prefix -> (input_price, output_price)  USD per 1M tokens
PRICES = {
    # OpenAI
    "gpt-4o": (2.50, 10.00),
    "gpt-4o-mini": (0.15, 0.60),
    "gpt-4.1": (2.00, 8.00),
    "gpt-4.1-mini": (0.40, 1.60),
    "gpt-4.1-nano": (0.10, 0.40),
    "o3": (2.00, 8.00),
    "o4-mini": (1.10, 4.40),
    # Anthropic
    "claude-opus-4": (15.00, 75.00),
    "claude-sonnet-4": (3.00, 15.00),
    "claude-haiku-3.5": (0.80, 4.00),
    "claude-3-5-sonnet": (3.00, 15.00),
    "claude-3-5-haiku": (0.80, 4.00),
    # DeepSeek
    "deepseek-chat": (0.27, 1.10),
    "deepseek-reasoner": (0.55, 2.19),
}

DEFAULT_PRICE = (1.00, 3.00)  # fallback for unknown models


def lookup(model: str) -> tuple[float, float]:
    """Longest-prefix match against the price table."""
    best, hit = DEFAULT_PRICE, -1
    for prefix, price in PRICES.items():
        if model.startswith(prefix) and len(prefix) > hit:
            best, hit = price, len(prefix)
    return best


def price_of(model: str, input_tokens: int, output_tokens: int) -> float:
    ip, op = lookup(model)
    return (input_tokens * ip + output_tokens * op) / 1_000_000
