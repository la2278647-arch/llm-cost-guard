"""Core ledger: SQLite-backed usage tracking and budgets."""

from __future__ import annotations

import json
import os
import sqlite3
import time
from pathlib import Path

from .pricing import price_of

DEFAULT_DB = Path.home() / ".llm-cost-guard" / "ledger.db"


class BudgetExceeded(Exception):
    def __init__(self, period: str, spent: float, limit: float):
        super().__init__(f"{period} budget exceeded: ${spent:.4f} > ${limit:.2f}")
        self.period, self.spent, self.limit = period, spent, limit


class Tracker:
    def __init__(self, db_path: str | os.PathLike | None = None):
        path = Path(db_path or os.environ.get("LCG_DB", DEFAULT_DB))
        path.parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(path)
        self.db.execute(
            """CREATE TABLE IF NOT EXISTS usage(
               id INTEGER PRIMARY KEY, ts INTEGER, model TEXT,
               input_tokens INTEGER, output_tokens INTEGER,
               cost REAL, tag TEXT)"""
        )
        self.db.execute(
            "CREATE TABLE IF NOT EXISTS budgets(period TEXT PRIMARY KEY, amount REAL)"
        )
        self.db.commit()

    def close(self) -> None:
        self.db.close()

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        self.close()

    def log(self, model: str, input_tokens: int, output_tokens: int, tag: str = "") -> float:
        cost = price_of(model, input_tokens, output_tokens)
        self.db.execute(
            "INSERT INTO usage(ts,model,input_tokens,output_tokens,cost,tag) VALUES(?,?,?,?,?,?)",
            (int(time.time()), model, input_tokens, output_tokens, cost, tag),
        )
        self.db.commit()
        return cost

    def report(self, by: str | None = None) -> list[dict]:
        if by == "day":
            key = "strftime('%Y-%m-%d', ts, 'unixepoch')"
        elif by == "model":
            key = "model"
        elif by == "tag":
            key = "tag"
        else:
            key = "'total'"
        rows = self.db.execute(
            f"""SELECT {key} AS k, COUNT(*), SUM(input_tokens), SUM(output_tokens), SUM(cost)
                FROM usage GROUP BY k ORDER BY SUM(cost) DESC"""
        ).fetchall()
        return [
            {"key": k, "calls": c, "input_tokens": it or 0, "output_tokens": ot or 0, "cost_usd": round(co or 0, 6)}
            for k, c, it, ot, co in rows
        ]

    def _period_start(self, period: str) -> int:
        now = time.localtime()
        if period == "daily":
            t = time.mktime((now.tm_year, now.tm_mon, now.tm_mday, 0, 0, 0, 0, 0, -1))
        elif period == "weekly":
            d = now.tm_mday - now.tm_wday
            t = time.mktime((now.tm_year, now.tm_mon, d, 0, 0, 0, 0, 0, -1))
        else:  # monthly
            t = time.mktime((now.tm_year, now.tm_mon, 1, 0, 0, 0, 0, 0, -1))
        return int(t)

    def spent(self, period: str) -> float:
        (total,) = self.db.execute(
            "SELECT COALESCE(SUM(cost),0) FROM usage WHERE ts >= ?",
            (self._period_start(period),),
        ).fetchone()
        return total

    def set_budget(self, period: str, amount: float) -> None:
        assert period in ("daily", "weekly", "monthly")
        self.db.execute(
            "INSERT INTO budgets(period,amount) VALUES(?,?) "
            "ON CONFLICT(period) DO UPDATE SET amount=excluded.amount",
            (period, amount),
        )
        self.db.commit()

    def get_budgets(self) -> dict[str, float]:
        return dict(self.db.execute("SELECT period, amount FROM budgets").fetchall())

    def check_budget(self, daily_usd=None, weekly_usd=None, monthly_usd=None) -> None:
        limits = self.get_budgets()
        for period, explicit in (("daily", daily_usd), ("weekly", weekly_usd), ("monthly", monthly_usd)):
            limit = explicit if explicit is not None else limits.get(period)
            if limit is not None:
                spent = self.spent(period)
                if spent > limit:
                    raise BudgetExceeded(period, spent, limit)

    def to_json(self, by=None) -> str:
        return json.dumps(self.report(by=by), ensure_ascii=False, indent=2)
