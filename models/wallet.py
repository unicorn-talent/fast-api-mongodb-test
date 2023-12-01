from typing import List
from pydantic import BaseModel


class BalanceHistoryEntry(BaseModel):
    timestamp: str  # ISO formatted timestamp
    token_balance: str
    usd_balance: str

# Data model for API input
class Wallet(BaseModel):
    wallet: str
    token_balance: str
    usd_balance: str
    last_update_time: str
    balances_history: List[BalanceHistoryEntry]
