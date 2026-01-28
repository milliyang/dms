"""
Data Fetchers

Fetch historical data from external sources (YFinance, Futu, etc.)
"""

from .base import Fetcher
from .yfinance_fetcher import YFinanceFetcher

__all__ = [
    "Fetcher",
    "YFinanceFetcher",
]
