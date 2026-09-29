import keyword

OPERATORS = ("+", "-", "*", "/", "%")


class CalculatorError(Exception):
    pass


class InvalidFormatError(CalculatorError):
    pass


class UnknownVariableError(CalculatorError):
    pass


class DivisionByZeroError(CalculatorError):
    pass


class UnsupportedOperatorError(CalculatorError):
    pass


def operand(text, variables):
    if text.isidentifier():
        if text not in variables:
            raise UnknownVariableError(f"variable '{text}' is not defined")
        return variables[text]
    try:
        return int(text)
    except ValueError:
        pass
    try:
        return float(text)
    except ValueError:
        raise InvalidFormatError(f"'{text}' is not a valid operand")


def calculate(parts, variables):
    if len(parts) != 3:
        raise InvalidFormatError("expected: operand operator operand")
    left, op, right = parts
    if op not in OPERATORS:
        raise UnsupportedOperatorError(f"operator '{op}' is not supported")
    a = operand(left, variables)
    b = operand(right, variables)
    if op in ("/", "%") and b == 0:
        raise DivisionByZeroError("division by zero")
    try:
        if op == "+":
            result = a + b
        elif op == "-":
            result = a - b
        elif op == "*":
            result = a * b
        elif op == "/":
            result = a / b
        else:
            result = a % b
    except OverflowError:
        raise InvalidFormatError("result is out of range")
    assert isinstance(result, (int, float))
    return result


def assign(parts, variables):
    name = parts[0]
    if not name.isidentifier() or keyword.iskeyword(name):
        raise InvalidFormatError(f"'{name}' is not a valid variable name")
    rest = parts[2:]
    variables[name] = operand(rest[0], variables) if len(rest) == 1 else calculate(rest, variables)


def main():
    variables = {}
    while True:
        try:
            line = input().strip()
        except EOFError:
            break
        if line.lower() == "quit":
            break
        if not line:
            continue
        parts = line.split()
        try:
            if len(parts) >= 3 and parts[1] == "=":
                assign(parts, variables)
            else:
                print(calculate(parts, variables))
        except CalculatorError as error:
            print(f"{type(error).__name__}: {error}")


if __name__ == "__main__":
    main()
