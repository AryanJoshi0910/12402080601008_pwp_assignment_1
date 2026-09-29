import heapq
import queue
import sys
import threading


def schedule(workers, jobs):
    jobs = sorted(jobs, key=lambda job: job[0])
    free = [(0, w) for w in range(1, workers + 1)]
    heapq.heapify(free)
    ready = []
    plan = []
    clock = 0
    i = 0
    while len(plan) < len(jobs):
        free_time, worker = heapq.heappop(free)
        now = max(free_time, clock)
        if not ready and i < len(jobs) and jobs[i][0] > now:
            now = jobs[i][0]
        while i < len(jobs) and jobs[i][0] <= now:
            arrival, job_id, priority, duration, _ = jobs[i]
            heapq.heappush(ready, (-priority, arrival, i, job_id, duration))
            i += 1
        _, arrival, _, job_id, duration = heapq.heappop(ready)
        clock = now
        plan.append((len(plan), job_id, worker, now, now + duration, now - arrival))
        heapq.heappush(free, (now + duration, worker))
    return plan


def worker_loop(tasks, lock, report):
    while True:
        item = tasks.get()
        if item is None:
            return
        with lock:
            report.append(item)


def execute(workers, plan):
    lock = threading.Lock()
    report = []
    inboxes = [queue.Queue() for _ in range(workers)]
    threads = [threading.Thread(target=worker_loop, args=(box, lock, report)) for box in inboxes]
    for thread in threads:
        thread.start()
    for item in plan:
        inboxes[item[2] - 1].put(item)
    for box in inboxes:
        box.put(None)
    for thread in threads:
        thread.join()
    return sorted(report)


def read_input():
    tokens = sys.stdin.read().split()
    w, n = int(tokens[0]), int(tokens[1])
    if not (1 <= w <= 64 and 1 <= n <= 200000):
        raise ValueError("w or n out of range")
    jobs = []
    pos = 2
    for _ in range(n):
        arrival, job_id = int(tokens[pos]), tokens[pos + 1]
        priority, duration, resources = int(tokens[pos + 2]), int(tokens[pos + 3]), int(tokens[pos + 4])
        pos += 5
        if arrival < 0 or not 1 <= duration <= 10**6 or not 1 <= resources <= 100:
            raise ValueError("invalid values for job " + job_id)
        jobs.append((arrival, job_id, priority, duration, resources))
    return w, jobs


def main():
    try:
        workers, jobs = read_input()
    except (ValueError, IndexError) as error:
        print("INVALID INPUT:", error)
        sys.exit(1)
    report = execute(workers, schedule(workers, jobs))
    for _, job_id, worker, start, finish, _ in report:
        print(f"{job_id} W{worker} {start} {finish}")
    print(f"AVG_WAIT {sum(item[5] for item in report) / len(report):.2f}")


if __name__ == "__main__":
    main()
