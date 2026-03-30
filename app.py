"""
app.py - Command-line interface for the Expense Categorizer
Usage:
    python app.py --file data/my_expenses.csv          # categorize a CSV
    python app.py --file data/my_expenses.csv --col description
    python app.py --desc "Uber ride to airport"        # classify one description
    python app.py --demo                               # run on sample data
    python app.py --file data/my_expenses.csv --summary  # show spending summary
"""

import argparse
import os
import sys
import pandas as pd
from categorize import categorize, categorize_csv, CATEGORY_EMOJI

BANNER = """
╔══════════════════════════════════════════════════════╗
║        💸  EXPENSE AUTO-CATEGORIZER  💸             ║
║   Classify your expenses with Machine Learning       ║
╚══════════════════════════════════════════════════════╝
"""


# ── Helpers ───────────────────────────────────────────────────────────────────

def print_single(description: str):
    result = categorize(description)
    print(f"\n  Description : {description}")
    print(f"  Category    : {result['emoji']}  {result['category']}  ({result['confidence']}% confidence)")
    print(f"  Top 3 guesses:")
    for cat, conf in result['top3']:
        bar = '█' * int(conf / 5) + '░' * (20 - int(conf / 5))
        print(f"    {CATEGORY_EMOJI.get(cat,'📦')} {cat:<25} {bar} {conf:.1f}%")
    print()


def print_table(df: pd.DataFrame, desc_col: str, n: int = None):
    rows = df if n is None else df.head(n)
    print(f"\n  {'#':<4} {'Description':<35} {'Category':<22} {'Conf':>6}")
    print("  " + "─" * 70)
    for i, row in rows.iterrows():
        desc = str(row[desc_col])[:33]
        cat  = f"{row['emoji']} {row['category']}"
        print(f"  {i+1:<4} {desc:<35} {cat:<22} {row['confidence']:>5.1f}%")
    print()


def print_summary(df: pd.DataFrame):
    print("\n  ── SPENDING SUMMARY ──────────────────────────────────────")

    # Try to find an amount column
    amount_col = None
    for col in df.columns:
        if col.lower() in ('amount', 'price', 'cost', 'total', 'value', 'spend'):
            amount_col = col
            break

    if amount_col:
        df[amount_col] = pd.to_numeric(df[amount_col], errors='coerce').fillna(0)
        summary = df.groupby('category')[amount_col].agg(['sum', 'count'])
        summary.columns = ['total_spent', 'transactions']
        summary = summary.sort_values('total_spent', ascending=False)
        total = summary['total_spent'].sum()

        print(f"\n  {'Category':<25} {'Txns':>5}  {'Amount':>10}  {'Share':>7}")
        print("  " + "─" * 55)
        for cat, row in summary.iterrows():
            pct  = row['total_spent'] / total * 100 if total else 0
            bar  = '█' * int(pct / 5)
            emoji = CATEGORY_EMOJI.get(cat, '📦')
            print(f"  {emoji} {cat:<22} {int(row['transactions']):>5}  "
                  f"₹{row['total_spent']:>9,.0f}  {pct:>6.1f}%  {bar}")
        print("  " + "─" * 55)
        print(f"  {'TOTAL':<25} {int(summary['transactions'].sum()):>5}  "
              f"₹{total:>9,.0f}")
    else:
        # Just show category counts
        summary = df['category'].value_counts()
        print(f"\n  {'Category':<25} {'Transactions':>12}")
        print("  " + "─" * 40)
        for cat, count in summary.items():
            emoji = CATEGORY_EMOJI.get(cat, '📦')
            bar   = '█' * count
            print(f"  {emoji} {cat:<22} {count:>12}  {bar}")
    print()


def save_output(df: pd.DataFrame, input_path: str):
    base    = os.path.splitext(input_path)[0]
    outpath = f"{base}_categorized.csv"
    df.to_csv(outpath, index=False)
    print(f"  ✅  Saved categorized file → {outpath}")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Expense Auto-Categorizer — classify expense descriptions using ML.'
    )
    parser.add_argument('--file',    type=str, help='Path to your expenses CSV file')
    parser.add_argument('--col',     type=str, default=None,
                        help='Name of the description column (auto-detected if omitted)')
    parser.add_argument('--desc',    type=str, help='Classify a single description string')
    parser.add_argument('--demo',    action='store_true', help='Run on the sample expenses CSV')
    parser.add_argument('--summary', action='store_true',
                        help='Show a spending summary after categorizing')
    parser.add_argument('--save',    action='store_true',
                        help='Save the categorized output to a new CSV')
    args = parser.parse_args()

    print(BANNER)

    # ── Single description ────────────────────────────────────────────────────
    if args.desc:
        try:
            print_single(args.desc)
        except FileNotFoundError as e:
            print(f"[ERROR] {e}")
            sys.exit(1)
        return

    # ── Demo mode ─────────────────────────────────────────────────────────────
    if args.demo:
        args.file = os.path.join('data', 'my_expenses.csv')
        args.summary = True

    # ── CSV mode ──────────────────────────────────────────────────────────────
    if args.file:
        if not os.path.exists(args.file):
            print(f"[ERROR] File not found: {args.file}")
            sys.exit(1)

        print(f"  Loading '{args.file}' ...")
        try:
            df, desc_col = categorize_csv(args.file, args.col)
        except (FileNotFoundError, ValueError) as e:
            print(f"[ERROR] {e}")
            sys.exit(1)

        print_table(df, desc_col)

        if args.summary:
            print_summary(df)

        if args.save:
            save_output(df, args.file)

        return

    # ── No args → interactive single-description mode ─────────────────────────
    print("  No arguments given — entering interactive mode.")
    print("  Type 'quit' to exit.\n")
    while True:
        try:
            desc = input("  Enter expense description: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break
        if desc.lower() in ('quit', 'exit', 'q'):
            print("Goodbye!")
            break
        if not desc:
            continue
        try:
            print_single(desc)
        except FileNotFoundError as e:
            print(f"[ERROR] {e}")
            sys.exit(1)


if __name__ == '__main__':
    main()
