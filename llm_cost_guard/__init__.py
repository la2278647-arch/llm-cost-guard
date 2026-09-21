"""llm-cost-guard: track, budget, and control LLM API spending."""

from .pricing import PRICES, price_of, lookup
from .tracker import Tracker, BudgetExceeded

__version__ = "0.1.0"
__all__ = ["Tracker", "BudgetExceeded", "price_of", "lookup", "PRICES", "__version__"]
