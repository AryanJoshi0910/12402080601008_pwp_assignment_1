import csv
import sys
from datetime import datetime
from decimal import Decimal, InvalidOperation

HEADER = ["transaction_id", "account_id", "type", "amount", "timestamp"]


class RowError(Exception):
    pass


def validate(row):
    if len(row) != 5:
        raise RowError("expected 5 columns")
    tid, account, kind, amount, stamp = (x.strip() for x in row)
    if not tid or not account:
        raise RowError("missing transaction or account id")
    if kind not in ("CREDIT", "DEBIT"):
        raise RowError("type must be CREDIT or DEBIT")
    try:
        value = Decimal(amount)
    except InvalidOperation:
        raise RowError("amount is not numeric")
    if not value.is_finite() or value <= 0:
        raise RowError("amount must be a positive number")
    try:
        datetime.strptime(stamp, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        raise RowError("timestamp must be yyyy-mm-ddThh:mm:ss")
    return [tid, account, kind, amount, stamp], value


def show(total):
    return format(total.normalize(), "f")


def main():
    path = input().strip()
    balances = {}
    try:
        with open(path, newline="", encoding="utf-8") as source, \
                open("credit.csv", "w", newline="", encoding="utf-8") as credit_file, \
                open("debit.csv", "w", newline="", encoding="utf-8") as debit_file, \
                open("error.csv", "w", newline="", encoding="utf-8") as error_file:
            credit = csv.writer(credit_file)
            debit = csv.writer(debit_file)
            errors = csv.writer(error_file)
            credit.writerow(HEADER)
            debit.writerow(HEADER)
            errors.writerow(HEADER + ["reason"])
            reader = csv.reader(source)
            next(reader, None)
            for row in reader:
                if not row:
                    continue
                try:
                    fields, value = validate(row)
                except RowError as error:
                    errors.writerow(row + [str(error)])
                    continue
                if fields[2] == "CREDIT":
                    credit.writerow(fields)
                    balances[fields[1]] = balances.get(fields[1], Decimal(0)) + value
                else:
                    debit.writerow(fields)
                    balances[fields[1]] = balances.get(fields[1], Decimal(0)) - value
    except (OSError, UnicodeDecodeError, csv.Error) as error:
        print("FILE ERROR:", error)
        sys.exit(1)
    for account, total in sorted(balances.items(), key=lambda item: (-abs(item[1]), item[0])):
        print(account, show(total))


if __name__ == "__main__":
    main()
