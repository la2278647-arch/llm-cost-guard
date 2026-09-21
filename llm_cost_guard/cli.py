"""lcg command line interface."""

from __future__ import annotations

import argparse
import sys

from .pricing import PRICES, price_of
from .tracker import Tracker, BudgetExceeded


def _print_table(rows):
    if not rows:
        print("(no usage recorded yet)")
        return
    headers = ["key", "calls", "input_tokens", "output_tokens", "cost_usd"]
    widths = [max(len(str(h)), *(len(str(r[h])) for r in rows)) for h in headers]
    print("  ".join(h.ljust(w) for h, w in zip(headers, widths)))
    for r in rows:
        print("  ".join(str(r[h]).ljust(w) for h, w in zip(headers, widths)))


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="lcg", description="LLM cost guard: track & budget LLM API spend")
    p.add_argument("--db", help="SQLite db path (default ~/.llm-cost-guard/ledger.db)")
    sub = p.add_subparsers(dest="cmd", required=True)

    plog = sub.add_parser("log", help="record a call")
    plog.add_argument("--model", required=True)
    plog.add_argument("--input-tokens", type=int, required=True)
    plog.add_argument("--output-tokens", type=int, required=True)
    plog.add_argument("--tag", default="")

    prep = sub.add_parser("report")
    prep.add_argument("--by", choices=["day", "model", "tag"])
    prep.add_argument("--json", action="store_true")

    pbud = sub.add_parser("budget")
    bsub = pbud.add_subparsers(dest="bcmd", required=True)
    bset = bsub.add_parser("set")
    bset.add_argument("--daily", type=float)
    bset.add_argument("--weekly", type=float)
    bset.add_argument("--monthly", type=float)
    bsub.add_parser("check")
    bsub.add_parser("show")

    pp = sub.add_parser("prices")
    psub = pp.add_subparsers(dest="pcmd")
    padd = psub.add_parser("add")
    padd.add_argument("model")
    padd.add_argument("--input", type=float, required=True)
    padd.add_argument("--output", type=float, required=True)

    pcalc = sub.add_parser("calc", help="estimate cost without recording")
    pcalc.add_argument("--model", required=True)
    pcalc.add_argument("--input-tokens", type=int, required=True)
    pcalc.add_argument("--output-tokens", type=int, required=True)

    args = p.parse_args(argv)
    t = Tracker(args.db)

    if args.cmd == "log":
        cost = t.log(args.model, args.input_tokens, args.output_tokens, args.tag)
        print(f"logged: ${cost:.6f}")
    elif args.cmd == "report":
        if args.json:
            print(t.to_json(by=args.by))
        else:
            _print_table(t.report(by=args.by))
    elif args.cmd == "budget":
        if args.bcmd == "set":
            for period in ("daily", "weekly", "monthly"):
                v = getattr(args, period)
                if v is not None:
                    t.set_budget(period, v)
                    print(f"{period} budget = ${v:.2f}")
        elif args.bcmd == "show":
            print(t.get_budgets() or "(no budgets set)")
        else:
            try:
                t.check_budget()
            except BudgetExceeded as e:
                print(f"BUDGET EXCEEDED: {e}", file=sys.stderr)
                return 2
            print("within budget")
    elif args.cmd == "prices":
        if args.pcmd == "add":
            PRICES[args.model] = (args.input, args.output)
            print(f"note: runtime-only for now; edit llm_cost_guard/pricing.py to persist "
                  f"{args.model}=({args.input},{args.output})")
        else:
            for m, (i, o) in sorted(PRICES.items()):
                print(f"{m:<24} in=${i}/M  out=${o}/M")
    elif args.cmd == "calc":
        print(f"${price_of(args.model, args.input_tokens, args.output_tokens):.6f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
