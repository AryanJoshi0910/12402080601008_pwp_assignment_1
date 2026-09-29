import re
import sys
import threading

TOKEN = re.compile(r"[0-9]+|[A-Za-z_][A-Za-z_0-9]*|[-+*()]|\S")
NUMBER = re.compile(r"[0-9]+")
NAME = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")


class Cycle(Exception):
    pass


class Invalid(Exception):
    pass


class Engine:
    def __init__(self, definitions):
        self.definitions = definitions
        self.memo = {}
        self.active = set()

    def lookup(self, name):
        if name in self.memo:
            return self.memo[name]
        if name in self.active:
            raise Cycle()
        if name not in self.definitions:
            raise Invalid()
        self.active.add(name)
        value = self.evaluate(TOKEN.findall(self.definitions[name]))
        self.active.discard(name)
        self.memo[name] = value
        return value

    def evaluate(self, tokens):
        pos = [0]

        def peek():
            return tokens[pos[0]] if pos[0] < len(tokens) else None

        def take():
            token = peek()
            pos[0] += 1
            return token

        def expression():
            value = term()
            while peek() in ("+", "-"):
                op = take()
                right = term()
                value = value + right if op == "+" else value - right
            return value

        def term():
            value = factor()
            while peek() == "*":
                take()
                value *= factor()
            return value

        def factor():
            token = take()
            if token is None:
                raise Invalid()
            if NUMBER.fullmatch(token):
                return int(token)
            if token == "(":
                value = expression()
                if take() != ")":
                    raise Invalid()
                return value
            if NAME.fullmatch(token):
                return self.lookup(token)
            raise Invalid()

        result = expression()
        if pos[0] != len(tokens):
            raise Invalid()
        return result


def main():
    lines = sys.stdin.read().split("\n")
    try:
        v = int(lines[0])
        definitions = {}
        for i in range(1, v + 1):
            name, _, body = lines[i].partition("=")
            definitions[name.strip()] = body
        target = lines[v + 1]
        print(Engine(definitions).evaluate(TOKEN.findall(target)))
    except Cycle:
        print("CYCLE")
    except (Invalid, ValueError, IndexError, RecursionError):
        print("INVALID")


if __name__ == "__main__":
    sys.setrecursionlimit(10**7)
    threading.stack_size(256 * 1024 * 1024)
    worker = threading.Thread(target=main)
    worker.start()
    worker.join()
