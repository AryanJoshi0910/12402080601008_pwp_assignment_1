# Programming with Python (202044504) - Assignment 1

B.Tech. Information Technology, Semester V

## Requirements

- Python 3.10 or above
- No external packages
- Q10 needs Tkinter (bundled with the standard Python installer on Windows and macOS; on Ubuntu run `sudo apt install python3-tk`)

## Files

| File | Question |
|------|----------|
| 12402080601008_1_Q1.py | Campus Merit Analyzer |
| 12402080601008_1_Q2.py | Password Audit (Aho-Corasick + regex) |
| 12402080601008_1_Q3.py | Recursive Expression Engine |
| 12402080601008_1_Q4.py | CSV Transaction Splitter |
| 12402080601008_1_Q5.py | Bank Settlement System |
| 12402080601008_1_Q6.py | Module Dependency Resolver |
| 12402080601008_1_Q7.py | Formula Validator |
| 12402080601008_1_Q8.py | Compressed Log Index |
| 12402080601008_1_Q9.py | Threaded Job Scheduler |
| 12402080601008_1_Q10.py | Tkinter Assignment Tracker |

## How to run

Q1, Q2, Q3, Q5, Q6, Q9 read from standard input:

```
python 12402080601008_1_Q1.py < tests/Q1_1.in
```

Q7 is interactive (type formulas, finish with `quit`), or:

```
python 12402080601008_1_Q7.py < tests/Q7_1.in
```

Q4 asks for the CSV path and writes `credit.csv`, `debit.csv`, `error.csv` in the current folder:

```
cd tests/Q4
echo transactions.csv | python ../../12402080601008_1_Q4.py
```

Q8 (run from `tests/Q8`). BUILD also writes `archive.pkl` next to `archive.zip`:

```
echo "BUILD logs archive.zip" | python ../../Enrollment_1_Q8.py
echo "SEARCH archive.pkl 3 error db missing" | python ../../12402080601008_1_Q8.py
```

Q10 opens a window and stores data in `assignment_tracker.json`:

```
python 12402080601008_1_Q10.py
```

## Tests

`tests/QN_k.in` is the input and `tests/QN_k.out` is the output produced by the program.
Test 1 of each question is the sample from the assignment; the rest are boundary and self-created cases (ties, cycles, invalid input, empty results).

## Assumptions and notes

- Q1: the tie-break rule is followed exactly (CPI, then higher average marks, then smaller enrollment). For the sample input, Chaitra (2203) has total marks 271 against Esha's (2205) 269, so the program prints `Semester 3: 2203 2205`, which differs from the sample output in the assignment PDF.
- Q2: checks run in this order: length, banned word, pattern (missing character class or 4+ repeated characters).
- Q3: unary minus is treated as invalid syntax. An undefined variable gives `INVALID`. Recursion depth is raised for long dependency chains.
- Q4: money is handled with `Decimal`. Rejected rows go to `error.csv` with a reason column.
- Q5: a failing operation outside a batch is skipped. A failing operation inside a batch rolls back the whole batch and prints `FAILED <batch number>`.
- Q6: import lines may be `a b` or `a imports b` (a imports b, so b loads first). One cycle is printed after `CYCLE`.
- Q7: `x = 10` and `x = a + b` are accepted. Errors print `ExceptionName: message`.
- Q9: jobs are assigned by a single dispatcher, then worker threads record their jobs in a lock-protected report. The resource count is validated (1 to 100) but does not affect scheduling.
- Q10: Export CSV writes the rows currently shown by the Pending / Completed / All filter. Marks are validated against the "Out of" value (default 20).

## Complexity

| Q | Time | Space |
|---|------|-------|
| 1 | O(n*m + n log k) | O(n*m) |
| 2 | O(total password length + total banned length) | O(total banned length) |
| 3 | O(total expression length) | O(total expression length) |
| 4 | O(r log a) | O(a) |
| 5 | O(q + n log n) | O(n + batch size) |
| 6 | O((n+e) log n) | O(n+e) |
| 7 | O(1) per formula | O(v) |
| 8 | O(total characters) | O(unique tokens + postings) |
| 9 | O(n log n) | O(n + w) |
| 10 | O(r) per filter or export | O(r) |
