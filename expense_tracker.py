"""
Group Expense Tracker
======================

This little script helps a group settle shared expenses.
It shows who paid, who owes money, and the easiest way to settle up.
"""

from collections import defaultdict


# ── 1. DATA: 5 friends, 8 shared expenses ───────────────────────────────────────

friends = ["Anmol", "Sanjay", "Niraj", "Manish", "Gaurav"]

expenses = [
    {"payer": "Anmol",   "amount": 120.00, "participants": ["Anmol", "Sanjay", "Niraj", "Manish", "Gaurav"]},
    {"payer": "Sanjay",  "amount": 45.00,  "participants": ["Sanjay", "Niraj", "Manish"]},
    {"payer": "Niraj",   "amount": 80.00,  "participants": ["Anmol", "Niraj", "Gaurav"]},
    {"payer": "Manish",  "amount": 30.00,  "participants": ["Anmol", "Sanjay", "Manish"]},
    {"payer": "Gaurav",  "amount": 96.00,  "participants": ["Sanjay", "Niraj", "Manish", "Gaurav"]},
    {"payer": "Anmol",   "amount": 50.00,  "participants": ["Anmol", "Sanjay", "Gaurav"]},
    {"payer": "Sanjay",  "amount": 70.00,  "participants": ["Anmol", "Sanjay", "Niraj", "Manish"]},
    {"payer": "Niraj",   "amount": 33.00,  "participants": ["Niraj", "Manish", "Gaurav"]},
]


# ── 2. CALCULATE NET BALANCES ──────────────────────────────────────────────────

def calculate_balances(expenses):
    """Work out how much each friend owes or is owed."""
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
    """Create a short list of payments to settle the group."""
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

    print("\n📋 EXPENSES")
    for index, exp in enumerate(expenses, start=1):
        share = exp["amount"] / len(exp["participants"])
        print(f"  {index}. {exp['payer']} paid ${exp['amount']:.2f} "
              f"for {exp['participants']} → ${share:.2f} each")

    print("\n💰 NET BALANCES")
    for person, bal in sorted(balances.items()):
        if bal > 0:
            status = f"is owed ${bal:.2f}"
        elif bal < 0:
            status = f"owes ${abs(bal):.2f}"
        else:
            status = "is all settled"
        print(f"  {person:<10} {status}")

    print(f"\n✅ SETTLEMENT PLAN ({len(transactions)} payments)")
    for debtor, creditor, amount in transactions:
        print(f"  {debtor} pays {creditor} ${amount:.2f}")

    print("\n" + "=" * 50)
    print(f"  Total payments needed: {len(transactions)}")
    print("=" * 50)


def visualize(balances, transactions):
    print("\n📊 VISUALIZATION")
    print("-" * 50)

    max_amount = max(abs(value) for value in balances.values()) if balances else 0
    scale = 30 / max_amount if max_amount else 1

    for person, bal in sorted(balances.items()):
        bar = "█" * int(abs(bal) * scale)
        sign = "+" if bal >= 0 else "-"
        print(f"  {person:<10} {sign} ${abs(bal):.2f} |{bar}")

    print("\n  Suggested payments:")
    for debtor, creditor, amount in transactions:
        print(f"    {debtor} → {creditor} : ${amount:.2f}")

    try:
        import matplotlib.pyplot as plt

        names = list(balances.keys())
        values = [balances[name] for name in names]
        colors = ["#2ca02c" if value >= 0 else "#d62728" for value in values]

        fig, ax = plt.subplots(figsize=(8, 4))
        ax.bar(names, values, color=colors)
        ax.axhline(0, color="black", linewidth=0.8)
        ax.set_ylabel("Net balance ($)")
        ax.set_title("Group Expense Balances")
        ax.grid(axis="y", linestyle="--", alpha=0.4)
        fig.tight_layout()

        output_path = "expense_balances.png"
        fig.savefig(output_path)
        plt.close(fig)
        print(f"\n  Chart saved to: {output_path}")
    except ImportError:
        print("\n  Tip: install matplotlib if you want a saved chart image.")


# ── 5. RUN ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    balances     = calculate_balances(expenses)
    transactions = settle(balances)
    display(balances, transactions)
    visualize(balances, transactions)