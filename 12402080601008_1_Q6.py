import heapq
import sys


def find_cycle(imports, pending):
    remaining = {name for name, count in pending.items() if count > 0}
    current = min(remaining)
    seen = {}
    path = []
    while current not in seen:
        seen[current] = len(path)
        path.append(current)
        current = min(dep for dep in imports[current] if dep in remaining)
    return path[seen[current]:]


def main():
    lines = [line.split() for line in sys.stdin.read().split("\n") if line.strip()]
    try:
        n, e = int(lines[0][0]), int(lines[0][1])
        modules = list(dict.fromkeys(line[0] for line in lines[1:1 + n]))
        known = set(modules)
        imports = {name: set() for name in modules}
        for line in lines[1 + n:1 + n + e]:
            a, b = line[0], line[-1]
            if len(line) not in (2, 3) or a not in known or b not in known:
                raise ValueError("bad import line: " + " ".join(line))
            imports[a].add(b)
    except (ValueError, IndexError) as error:
        print("INVALID INPUT:", error)
        sys.exit(1)
    dependents = {name: [] for name in modules}
    pending = {}
    for name, deps in imports.items():
        pending[name] = len(deps)
        for dep in deps:
            dependents[dep].append(name)
    heap = [name for name in modules if pending[name] == 0]
    heapq.heapify(heap)
    order = []
    while heap:
        current = heapq.heappop(heap)
        order.append(current)
        for user in dependents[current]:
            pending[user] -= 1
            if pending[user] == 0:
                heapq.heappush(heap, user)
    if len(order) == len(modules):
        print(" ".join(order))
    else:
        print("CYCLE", " ".join(find_cycle(imports, pending)))


if __name__ == "__main__":
    main()
