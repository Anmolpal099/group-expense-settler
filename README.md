# Group Expense Tracker

A friendly Python script for a group of friends who want to split shared expenses and settle up cleanly.

---

## Quick Demo

Run the script and see something like this:

```
==================================================
       GROUP EXPENSE TRACKER
==================================================

📋 EXPENSES:
  1. Anmol paid $120.00 for ['Anmol', 'Sanjay', 'Niraj', 'Manish', 'Gaurav'] → $24.00/person
  2. Sanjay paid $45.00 for ['Sanjay', 'Niraj', 'Manish'] → $15.00/person
  3. Niraj paid $80.00 for ['Anmol', 'Niraj', 'Gaurav'] → $26.67/person
  4. Manish paid $30.00 for ['Anmol', 'Sanjay', 'Manish'] → $10.00/person
  5. Gaurav paid $96.00 for ['Sanjay', 'Niraj', 'Manish', 'Gaurav'] → $24.00/person
  6. Anmol paid $50.00 for ['Anmol', 'Sanjay', 'Gaurav'] → $16.67/person
  7. Sanjay paid $70.00 for ['Anmol', 'Sanjay', 'Niraj', 'Manish'] → $17.50/person
  8. Niraj paid $33.00 for ['Niraj', 'Manish', 'Gaurav'] → $11.00/person

💰 NET BALANCES:
  Anmol      is owed  $75.17
  Sanjay     is owed  $7.83
  Niraj      owes     $5.17
  Manish     owes     $71.50
  Gaurav     owes     $6.33

✅ SETTLEMENT PLAN (4 transactions):
  Manish pays Anmol $71.50
  Gaurav pays Sanjay $6.33
  Niraj pays Anmol $3.67
  Niraj pays Sanjay $1.50

==================================================
  Total transactions needed: 4
==================================================

📊 VISUALIZATION
--------------------------------------------------
  Anmol      + $75.17 |██████████████████████████████
  Sanjay     + $7.83 |███
  Niraj      - $5.17 |██
  Manish     - $71.50 |████████████████████████████
  Gaurav     - $6.33 |██

  Settlement flow:
    Manish → Anmol : $71.50
    Gaurav → Sanjay : $6.33
    Niraj → Anmol : $3.67
    Niraj → Sanjay : $1.50

  Install matplotlib to save a bar chart image: python -m pip install matplotlib
```

---

## How to Run

Open a terminal inside this folder and run:

```bash
python ./expense_tracker.py
```

That’s it — the script runs with plain Python. If you want a saved chart image, install `matplotlib`.

---

## What this does

This project helps you see:

- who paid for each expense,
- who owes money,
- who is owed money,
- and the easiest way to settle up.

It works for a small group and keeps the math clean so the totals always balance.

---

## Who is in the example

This demo uses five friends:

- Anmol
- Sanjay
- Niraj
- Manish
- Gaurav

They share eight expenses in the example data.

---

## How it works

1. Every expense is split equally among the people involved.
2. The person who paid gets credit for the full amount.
3. Each person’s final balance becomes either:
   - positive (they should receive money), or
   - negative (they need to pay money).
4. The script then suggests simple payments that settle the group quickly.

---

## Why the balances stay clean

Some expense splits do not divide evenly into cents. The code:

- calculates with full precision,
- rounds each final balance to two decimals,
- and adjusts any tiny leftover cent so the total stays at zero.

That keeps the result fair and exact.

---

## What the output shows

The script prints:

- a list of the shared expenses,
- each person’s net balance,
- a settlement plan showing who pays whom,
- and a simple text-based bar chart.

If `matplotlib` is installed, it also saves a bar chart image as `expense_balances.png`.

### Net Balances Example

| Person  | Balance   | Status              |
|---------|-----------|---------------------|
| Anmol   | +$75.17   | Is owed money ✅    |
| Sanjay  | +$7.83    | Is owed money ✅    |
| Niraj   | −$5.17    | Owes money ❌       |
| Manish  | −$71.50   | Owes money ❌       |
| Gaurav  | −$6.33    | Owes money ❌       |

### Settlement Plan Example

| From   | To    | Amount  |
|--------|-------|---------|
| Manish | Anmol | $71.50  |
| Gaurav | Sanjay| $6.33   |
| Niraj  | Anmol | $3.67   |
| Niraj  | Sanjay| $1.50   |

**Total transactions: 4** (the minimum possible for 5 people!)

---

## Visualization

The program includes a friendly terminal chart.
If you install `matplotlib`, it will also create a saved image.

To install it:

```bash
python -m pip install matplotlib
```

---

## Try it yourself

1. Clone or download this repo.
2. Run `python ./expense_tracker.py`.
3. See the results for the demo group.
4. Edit the `expenses` list in the code to add your own group's expenses.
5. Run again to see your custom settlement plan!

---

## Code structure

This project is just one file:

```
expense_tracker.py
│
├── friends[]              # The list of people in the group
├── expenses[]             # The example expense records
├── calculate_balances()   # Works out how much each person owes or is owed
├── settle()               # Builds a short settlement plan
├── display()              # Prints the results in a friendly way
└── visualize()            # Shows a text bar chart and optional image export
```

---
