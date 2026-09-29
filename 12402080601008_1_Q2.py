import re
import sys
from collections import deque


def build_automaton(words):
    goto = [{}]
    fail = [0]
    found = [False]
    for word in words:
        state = 0
        for ch in word:
            if ch not in goto[state]:
                goto.append({})
                fail.append(0)
                found.append(False)
                goto[state][ch] = len(goto) - 1
            state = goto[state][ch]
        found[state] = True
    queue = deque(goto[0].values())
    while queue:
        node = queue.popleft()
        for ch, child in goto[node].items():
            f = fail[node]
            while f and ch not in goto[f]:
                f = fail[f]
            fail[child] = goto[f].get(ch, 0)
            found[child] = found[child] or found[fail[child]]
            queue.append(child)
    return goto, fail, found


def contains_banned(text, automaton):
    goto, fail, found = automaton
    state = 0
    for ch in text:
        while state and ch not in goto[state]:
            state = fail[state]
        state = goto[state].get(ch, 0)
        if found[state]:
            return True
    return False


def has_all_classes(password):
    patterns = (r"[a-z]", r"[A-Z]", r"[0-9]", r"[$#@]")
    return all(re.search(p, password) for p in patterns)


def classify(password, automaton):
    if not 6 <= len(password) <= 12:
        return "WEAK_LENGTH"
    if contains_banned(password.lower(), automaton):
        return "COMPROMISED"
    if re.search(r"(.)\1{3}", password) or not has_all_classes(password):
        return "WEAK_PATTERN"
    return "STRONG"


def main():
    lines = [line.rstrip("\r") for line in sys.stdin.read().split("\n")]
    try:
        b = int(lines[0])
        banned = [w.strip().lower() for w in lines[1:1 + b] if w.strip()]
        n = int(lines[b + 1])
        if not (1 <= b <= 10000 and 1 <= n <= 100000):
            raise ValueError("b or n out of range")
    except (ValueError, IndexError) as error:
        print("INVALID INPUT:", error)
        sys.exit(1)
    passwords = lines[b + 2:b + 2 + n]
    passwords += [""] * (n - len(passwords))
    automaton = build_automaton(banned)
    print("\n".join(f"{i}: {classify(p, automaton)}" for i, p in enumerate(passwords, 1)))


if __name__ == "__main__":
    main()
