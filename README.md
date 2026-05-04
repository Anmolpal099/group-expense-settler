# Group Expense Tracker

A simple Python program that calculates who owes whom after a group trip — using the **fewest possible transactions**.

---

## How to Run

```bash
python ./expense_tracker.py
```

Or from the project directory:

```bash
python expense_tracker.py
```

Pure Python. Optional: `matplotlib` for chart visualization.

---

## What the Program Does

### Step 1 — Calculate Net Balances

For every expense, the **payer gets full credit**, and **each participant is charged their equal share**.

```
Net Balance = Total Paid  −  Total Share Owed
```

- **Positive balance** → this person is *owed* money  
- **Negative balance** → this person *owes* money  

---

### Step 2 — Settle with Fewest Transactions

The program uses a **greedy algorithm**:

1. Separate everyone into two groups: **creditors** (owed money) and **debtors** (owe money).
2. Always pick the **largest debtor** and **largest creditor**.
3. The debtor pays the creditor the **smaller of the two amounts**.
4. That fully settles at least one person (they reach zero).
5. Repeat until everyone is settled.

**Why this minimizes transactions:**  
Every single transaction fully eliminates at least one person from the list. So with N people who have non-zero balances, you need at most **N − 1 transactions** — which is the minimum possible.

**Example from our demo (5 people, 8 expenses):**
```
Manish   pays Anmol   $71.50
Gaurav     pays Sanjay     $6.33
Niraj pays Anmol   $3.67
Niraj pays Sanjay     $1.50
```
Only **4 transactions** to fully settle 5 people. ✅

---

## Rounding Strategy

Expenses are sometimes split unevenly (e.g., $80 ÷ 3 = $26.666...).

**How we handle it:**
1. All calculations use full floating-point precision.
2. At the end, each person's balance is **rounded to 2 decimal places** (nearest cent).
3. We check if the sum of all balances equals exactly zero.
4. If there is a tiny residue (e.g., $0.01) due to rounding, it is **absorbed by the person with the largest absolute balance** — the person most involved financially, so it affects them the least proportionally.

**Why this is fair:**  
The residue is always at most a few cents across the whole group. Placing it on the largest balance person means it's a negligible adjustment (e.g., $0.01 on a $75 balance).

---

## Demo Data

| # | Payer   | Amount  | Participants                        | Share/person |
|---|---------|---------|-------------------------------------|--------------|
| 1 | Anmol   | $120.00 | Anmol, Sanjay, Niraj, Manish, Gaurav     | $24.00       |
| 2 | Sanjay     | $45.00  | Sanjay, Niraj, Manish                 | $15.00       |
| 3 | Niraj | $80.00  | Anmol, Niraj, Gaurav                 | $26.67       |
| 4 | Manish   | $30.00  | Anmol, Sanjay, Manish                   | $10.00       |
| 5 | Gaurav     | $96.00  | Sanjay, Niraj, Manish, Gaurav            | $24.00       |
| 6 | Anmol   | $50.00  | Anmol, Sanjay, Gaurav                     | $16.67       |
| 7 | Sanjay     | $70.00  | Anmol, Sanjay, Niraj, Manish          | $17.50       |
| 8 | Niraj | $33.00  | Niraj, Manish, Gaurav                 | $11.00       |

### Net Balances

| Person  | Balance   | Status              |
|---------|-----------|---------------------|
| Anmol   | +$75.17   | Is owed money ✅    |
| Sanjay     | +$7.83    | Is owed money ✅    |
| Niraj | −$5.17    | Owes money ❌       |
| Manish   | −$71.50   | Owes money ❌       |
| Gaurav     | −$6.33    | Owes money ❌       |

### Settlement Plan (4 transactions)

```
Manish   pays Anmol   $71.50
Gaurav     pays Sanjay     $6.33
Niraj pays Anmol   $3.67
Niraj pays Sanjay     $1.50
```

---

## Visualization

The script  includes a simple visualization step after computing balances.

- A text-based bar chart displays each person’s net balance.
- A settlement flow list shows who pays whom.
- If `matplotlib` is installed, the script also saves a bar chart image to `expense_balances.png`.

To install `matplotlib`:

```bash
python -m pip install matplotlib
```

---

## Code Structure

```
expense_tracker.py
│
├── expenses[]            # Input: 8 expense records
├── calculate_balances()  # Computes net balance per person
├── settle()              # Greedy algorithm → fewest transactions
├── display()             # Prints results clearly
└── visualize()           # Text bar chart + optional matplotlib chart
```

---
