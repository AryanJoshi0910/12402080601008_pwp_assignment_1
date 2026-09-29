import heapq
import sys


def read_input():
    data = sys.stdin.read().split()
    n, k, m = int(data[0]), int(data[1]), int(data[2])
    if not (1 <= n <= 100000 and 1 <= k <= 50 and 1 <= m <= 12):
        raise ValueError("n, k or m out of range")
    if len(data) < 3 + n * (4 + m):
        raise ValueError("fewer records than n")
    records = []
    pos = 3
    for _ in range(n):
        enrollment, name = data[pos], data[pos + 1]
        semester, cpi = int(data[pos + 2]), float(data[pos + 3])
        marks = tuple(int(x) for x in data[pos + 4:pos + 4 + m])
        pos += 4 + m
        if not (1 <= semester <= 8 and 0.0 <= cpi <= 10.0):
            raise ValueError("semester or CPI out of range for " + enrollment)
        if not all(0 <= x <= 100 for x in marks):
            raise ValueError("marks out of range for " + enrollment)
        records.append((enrollment, name, semester, cpi, marks))
    return k, m, records


def semester_toppers(records, k):
    groups = {}
    for enrollment, _, semester, cpi, marks in records:
        groups.setdefault(semester, []).append((-cpi, -sum(marks), enrollment))
    return {
        semester: [item[2] for item in heapq.nsmallest(k, items)]
        for semester, items in sorted(groups.items())
    }


def subject_toppers(records, m):
    best = [-1] * m
    winners = [[] for _ in range(m)]
    for enrollment, _, _, _, marks in records:
        for j in range(m):
            if marks[j] > best[j]:
                best[j] = marks[j]
                winners[j] = [enrollment]
            elif marks[j] == best[j]:
                winners[j].append(enrollment)
    return [sorted(group) for group in winners]


def main():
    try:
        k, m, records = read_input()
    except (ValueError, IndexError) as error:
        print("INVALID INPUT:", error)
        sys.exit(1)
    for semester, top in semester_toppers(records, k).items():
        print(f"Semester {semester}: {' '.join(top)}")
    for j, group in enumerate(subject_toppers(records, m), 1):
        print(f"S{j}: {' '.join(group)}")


if __name__ == "__main__":
    main()
