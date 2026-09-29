import sys


class BankError(Exception):
    pass


class InsufficientFundsError(BankError):
    pass


class AccountNotFoundError(BankError):
    pass


class InvalidAmountError(BankError):
    pass


class InvalidOperationError(BankError):
    pass


class Account:
    def __init__(self, account_id, balance):
        self._account_id = account_id
        self._balance = balance

    @property
    def account_id(self):
        return self._account_id

    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, value):
        if value < 0:
            raise InsufficientFundsError(self._account_id + " cannot go below zero")
        self._balance = value


class Transaction:
    def __init__(self, kind, source, target, amount):
        self.kind = kind
        self.source = source
        self.target = target
        self.amount = amount


class Bank:
    def __init__(self):
        self._accounts = {}
        self.history = []

    def add_account(self, account_id, balance):
        if balance < 0:
            raise InvalidAmountError("opening balance cannot be negative")
        self._accounts[account_id] = Account(account_id, balance)

    def find(self, account_id):
        if account_id not in self._accounts:
            raise AccountNotFoundError(account_id)
        return self._accounts[account_id]

    def execute(self, tx):
        if not 0 < tx.amount <= 10**9:
            raise InvalidAmountError(str(tx.amount))
        steps = []
        if tx.kind in ("WITHDRAW", "TRANSFER"):
            steps.append((self.find(tx.source), -tx.amount))
        if tx.kind in ("DEPOSIT", "TRANSFER"):
            steps.append((self.find(tx.target), tx.amount))
        done = []
        for account, delta in steps:
            account.balance += delta
            done.append((account, delta))
        self.history.append(tx)
        return done

    def rollback(self, steps, history_mark):
        for account, delta in reversed(steps):
            account.balance -= delta
        del self.history[history_mark:]

    def report(self):
        return [(key, self._accounts[key].balance) for key in sorted(self._accounts)]


def parse_operation(parts):
    kind = parts[0]
    if kind == "DEPOSIT":
        return Transaction(kind, None, parts[1], int(parts[2]))
    if kind == "WITHDRAW":
        return Transaction(kind, parts[1], None, int(parts[2]))
    if kind == "TRANSFER":
        return Transaction(kind, parts[1], parts[2], int(parts[3]))
    raise InvalidOperationError(kind)


def main():
    lines = sys.stdin.read().split("\n")
    bank = Bank()
    try:
        n = int(lines[0])
        for i in range(1, n + 1):
            account_id, balance = lines[i].split()
            bank.add_account(account_id, int(balance))
        q = int(lines[n + 1])
        operations = lines[n + 2:n + 2 + q]
    except (ValueError, IndexError, BankError) as error:
        print("INVALID INPUT:", error)
        sys.exit(1)
    failed = []
    batch_no = 0
    in_batch = False
    batch_failed = False
    batch_steps = []
    mark = 0
    for line in operations:
        parts = line.split()
        if not parts:
            continue
        command = parts[0]
        if command == "BATCH_BEGIN":
            if not in_batch:
                in_batch = True
                batch_no += 1
                batch_failed = False
                batch_steps = []
                mark = len(bank.history)
        elif command == "BATCH_END":
            if in_batch:
                if batch_failed:
                    bank.rollback(batch_steps, mark)
                    failed.append(batch_no)
                in_batch = False
        else:
            if in_batch and batch_failed:
                continue
            try:
                steps = bank.execute(parse_operation(parts))
            except (BankError, ValueError, IndexError):
                if in_batch:
                    batch_failed = True
                continue
            if in_batch:
                batch_steps.extend(steps)
    if in_batch:
        bank.rollback(batch_steps, mark)
        failed.append(batch_no)
    for number in failed:
        print("FAILED", number)
    for account_id, balance in bank.report():
        print(account_id, balance)


if __name__ == "__main__":
    main()
