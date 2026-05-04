"""
Group Expense Tracker - Settlement Calculator
==============================================
Rounding Strategy:
  - All balances are kept as floats during calculation.
  - At the end, each balance is rounded to 2 decimal places.
  - If total rounding causes a tiny imbalance (e.g., +0.01),
    it is absorbed by the person with the largest absolute balance.
  - This ensures all balances sum exactly to zero before settlement.
"""

from collections import defaultdict


# ── 1. DATA: 5 people, 8 expenses ─────────────────────────────────────────────

people = ["Alice", "Bob", "Charlie", "Diana", "Eve"]

expenses = [
    {"payer": "Alice",   "amount": 120.00, "participants": ["Alice", "Bob", "Charlie", "Diana", "Eve"]},
    {"payer": "Bob",     "amount": 45.00,  "participants": ["Bob", "Charlie", "Diana"]},
    {"payer": "Charlie", "amount": 80.00,  "participants": ["Alice", "Charlie", "Eve"]},
    {"payer": "Diana",   "amount": 30.00,  "participants": ["Alice", "Bob", "Diana"]},
    {"payer": "Eve",     "amount": 96.00,  "participants": ["Bob", "Charlie", "Diana", "Eve"]},
    {"payer": "Alice",   "amount": 50.00,  "participants": ["Alice", "Bob", "Eve"]},
    {"payer": "Bob",     "amount": 70.00,  "participants": ["Alice", "Bob", "Charlie", "Diana"]},
    {"payer": "Charlie", "amount": 33.00,  "participants": ["Charlie", "Diana", "Eve"]},
]


# ── 2. CALCULATE NET BALANCES ──────────────────────────────────────────────────

def calculate_balances(expenses):
    """
    For each expense:
      - The payer's balance increases by the full amount.
      - Each participant's balance decreases by their equal share.
    Net balance > 0  → person is owed money
    Net balance < 0  → person owes money
    """
    balance = defaultdict(float)

    for exp in expenses:
        payer        = exp["payer"]
        amount       = exp["amount"]
        participants = exp["participants"]
        share        = amount / len(participants)

        balance[payer] += amount          # payer gets credit
        for person in participants:
            balance[person] -= share      # everyone pays their share

    # Round each balance to 2 decimal places
    for person in balance:
        balance[person] = round(balance[person], 2)

    # Fix any tiny rounding residue so balances sum to exactly 0
    total = round(sum(balance.values()), 2)
    if total != 0.0:
        # Absorb residue into the person with the largest absolute balance
        adjust_person = max(balance, key=lambda p: abs(balance[p]))
        balance[adjust_person] = round(balance[adjust_person] - total, 2)

    return dict(balance)


# ── 3. SETTLE WITH FEWEST TRANSACTIONS ────────────────────────────────────────

def settle(balances):
    """
    Greedy algorithm to minimize transactions:
      1. Split everyone into creditors (owed money) and debtors (owe money).
      2. Always match the largest debtor with the largest creditor.
      3. The smaller of the two amounts settles; the remaining balance carries over.
      4. Repeat until all balances are zero.

    Why this minimizes transactions:
      Each transaction fully settles at least one person (either the debtor
      or creditor reaches zero). So the number of transactions is at most
      (number of people - 1), which is the theoretical minimum.
    """
    # Work with mutable copies, ignore anyone already at zero
    creditors = {p: b for p, b in balances.items() if b > 0}
    debtors   = {p: -b for p, b in balances.items() if b < 0}

    transactions = []

    while creditors and debtors:
        # Pick the largest on each side
        creditor = max(creditors, key=creditors.get)
        debtor   = max(debtors,   key=debtors.get)

        credit_amt = creditors[creditor]
        debt_amt   = debtors[debtor]

        # The transaction amount is the smaller of the two
        amount = min(credit_amt, debt_amt)
        amount = round(amount, 2)

        transactions.append((debtor, creditor, amount))

        # Update balances
        creditors[creditor] = round(credit_amt - amount, 2)
        debtors[debtor]     = round(debt_amt   - amount, 2)

        # Remove settled people
        if creditors[creditor] == 0:
            del creditors[creditor]
        if debtors[debtor] == 0:
            del debtors[debtor]

    return transactions


# ── 4. DISPLAY RESULTS ────────────────────────────────────────────────────────

def display(balances, transactions):
    print("=" * 50)
    print("       GROUP EXPENSE TRACKER")
    print("=" * 50)

    print("\n📋 EXPENSES:")
    for i, exp in enumerate(expenses, 1):
        share = exp["amount"] / len(exp["participants"])
        print(f"  {i}. {exp['payer']} paid ${exp['amount']:.2f} "
              f"for {exp['participants']} → ${share:.2f}/person")

    print("\n💰 NET BALANCES:")
    for person, bal in sorted(balances.items()):
        if bal > 0:
            status = f"is owed  ${bal:.2f}"
        elif bal < 0:
            status = f"owes     ${abs(bal):.2f}"
        else:
            status = "is settled"
        print(f"  {person:<10} {status}")

    print(f"\n✅ SETTLEMENT PLAN ({len(transactions)} transactions):")
    for debtor, creditor, amount in transactions:
        print(f"  {debtor} pays {creditor} ${amount:.2f}")

    print("\n" + "=" * 50)
    print(f"  Total transactions needed: {len(transactions)}")
    print("=" * 50)


# ── 5. RUN ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    balances     = calculate_balances(expenses)
    transactions = settle(balances)
    display(balances, transactions)