import os
import pickle
import re
import sys
import zipfile

TOKEN = re.compile(r"[a-z0-9_]+")
MAX_TOKEN = 50


def build(folder, zip_name):
    if not os.path.isdir(folder):
        raise FileNotFoundError(folder)
    names = sorted(
        f for f in os.listdir(folder)
        if os.path.isfile(os.path.join(folder, f)) and not f.endswith((".zip", ".pkl"))
    )
    index = {}
    total_lines = 0
    for name in names:
        with open(os.path.join(folder, name), encoding="utf-8", errors="ignore") as handle:
            for number, line in enumerate(handle, 1):
                total_lines += 1
                for token in set(TOKEN.findall(line.lower())):
                    if len(token) <= MAX_TOKEN:
                        index.setdefault(token, []).append((name, number))
    pickle_path = os.path.splitext(zip_name)[0] + ".pkl"
    with open(pickle_path, "wb") as handle:
        pickle.dump(index, handle)
    with zipfile.ZipFile(zip_name, "w", zipfile.ZIP_DEFLATED) as archive:
        for name in names:
            archive.write(os.path.join(folder, name), os.path.join("logs", name))
        archive.write(pickle_path, os.path.basename(pickle_path))
    print("FILES", len(names))
    print("LINES", total_lines)
    print("TOKENS", len(index))


def search(pickle_path, queries):
    with open(pickle_path, "rb") as handle:
        index = pickle.load(handle)
    for query in queries:
        hits = index.get(query.lower())
        if not hits:
            print(query, "NOT FOUND")
            continue
        for name, number in hits:
            print(f"{query} {name}:{number}")


def main():
    tokens = sys.stdin.read().split()
    try:
        mode = tokens[0].upper()
        if mode == "BUILD":
            build(tokens[1], tokens[2])
        elif mode == "SEARCH":
            count = int(tokens[2])
            search(tokens[1], tokens[3:3 + count])
        else:
            raise ValueError("mode must be BUILD or SEARCH")
    except (ValueError, IndexError) as error:
        print("INVALID INPUT:", error)
        sys.exit(1)
    except (OSError, pickle.UnpicklingError, EOFError) as error:
        print("FILE ERROR:", error)
        sys.exit(1)


if __name__ == "__main__":
    main()
