#!/usr/bin/env python3
"""Safe, idempotent bookmark maintenance for the Cortana Obsidian vault.

Maintains the hierarchical Bookmarks tree in the ACTIVE vault's
`.obsidian/bookmarks.json`. Use this instead of hand-editing the JSON — it
auto-detects the live vault, de-dupes, creates nested groups, backs up, and
re-validates after every write.

USAGE
  bookmark.py upsert --path cortana-vault/projects/x/x.md --group "Business/WaiveLabs" --title "X Hub"
  bookmark.py prune                 # drop bookmarks whose target file no longer exists
  bookmark.py list                  # print the current tree
  bookmark.py --vault /abs/VaultRoot <cmd>   # override auto-detection

NOTES
- Group path uses "/" (e.g. "Business/WaiveLabs/Marketing"); segments are matched
  ignoring a leading emoji, so "Business" matches an existing "💼 Business" group.
- `upsert` is idempotent: if --path is already bookmarked anywhere, it is MOVED to
  the target group and retitled rather than duplicated.
- Obsidian caches bookmarks on load — reload the vault / restart to see changes.
"""
import argparse, json, os, re, shutil, sys, time

# Candidate vault roots in priority order; the one with the most recently
# modified .obsidian/workspace.json wins. Add roots here if they change.
CANDIDATE_ROOTS = [
    os.path.expanduser("~/Cortana"),
    os.path.expanduser("~/Cortana/cortana-vault"),
]

def detect_vault(override=None):
    if override:
        return os.path.abspath(override)
    best, best_mt = None, -1
    for root in CANDIDATE_ROOTS:
        ws = os.path.join(root, ".obsidian", "workspace.json")
        bm = os.path.join(root, ".obsidian", "bookmarks.json")
        if not os.path.isfile(bm):
            continue
        mt = os.path.getmtime(ws) if os.path.isfile(ws) else 0
        if mt > best_mt:
            best, best_mt = root, mt
    if not best:
        sys.exit("No .obsidian/bookmarks.json found in candidate roots.")
    return best

def norm(title):
    # strip a leading emoji / symbol + whitespace, lowercase, for group matching
    return re.sub(r"^[^\w]+", "", title or "").strip().lower()

def load(bm_path):
    with open(bm_path) as f:
        return json.load(f)

def save(bm_path, data):
    bak = bm_path + ".bak"
    if os.path.isfile(bm_path):
        shutil.copy2(bm_path, bak)
    tmp = bm_path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    # validate before replacing
    with open(tmp) as f:
        json.load(f)
    os.replace(tmp, bm_path)

def find_and_remove(items, path):
    """Remove the file item with this path anywhere in the tree. Returns (removed_item|None)."""
    for i, it in enumerate(items):
        if it.get("type") == "file" and it.get("path") == path:
            return items.pop(i)
        if it.get("type") == "group":
            got = find_and_remove(it.get("items", []), path)
            if got:
                return got
    return None

def ensure_group(items, segments):
    """Descend/create nested groups by normalized title; return the deepest group's items list."""
    cur = items
    for seg in segments:
        match = None
        for it in cur:
            if it.get("type") == "group" and norm(it.get("title", "")) == norm(seg):
                match = it
                break
        if not match:
            match = {"type": "group", "ctime": int(time.time() * 1000), "title": seg, "items": []}
            cur.append(match)
        cur = match["items"]
    return cur

def cmd_upsert(data, args):
    if not args.path or not args.title:
        sys.exit("upsert requires --path and --title")
    existing = find_and_remove(data["items"], args.path)  # move semantics
    target = data["items"] if not args.group else ensure_group(data["items"], args.group.split("/"))
    entry = {"type": "file", "path": args.path, "title": args.title}
    if existing and existing.get("ctime"):
        entry["ctime"] = existing["ctime"]
    target.append(entry)
    print(("moved" if existing else "added") + f": {args.title}  →  {args.group or '(top)'}")

def cmd_prune(data, args):
    removed = []
    def walk(items):
        keep = []
        for it in items:
            if it.get("type") == "file":
                rel = it.get("path", "")
                if os.path.isfile(os.path.join(args._vault, rel)):
                    keep.append(it)
                else:
                    removed.append(rel)
            elif it.get("type") == "group":
                it["items"] = walk(it.get("items", []))
                keep.append(it)
            else:
                keep.append(it)
        return keep
    data["items"] = walk(data["items"])
    print(f"pruned {len(removed)} broken bookmark(s):")
    for r in removed:
        print("  -", r)

def cmd_list(data, args):
    def walk(items, d=0):
        for it in items:
            pad = "  " * d
            if it.get("type") == "group":
                print(f"{pad}▸ {it.get('title','')}")
                walk(it.get("items", []), d + 1)
            else:
                print(f"{pad}• {it.get('title','')}  ({it.get('path','')})")
    walk(data["items"])

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("command", choices=["upsert", "prune", "list"])
    ap.add_argument("--path"); ap.add_argument("--group"); ap.add_argument("--title")
    ap.add_argument("--vault", help="override active-vault detection")
    args = ap.parse_args()
    vault = detect_vault(args.vault)
    args._vault = vault
    bm_path = os.path.join(vault, ".obsidian", "bookmarks.json")
    data = load(bm_path)
    if "items" not in data or not isinstance(data["items"], list):
        sys.exit("Unexpected bookmarks.json shape (expected {'items': [...]}).")
    {"upsert": cmd_upsert, "prune": cmd_prune, "list": cmd_list}[args.command](data, args)
    if args.command != "list":
        save(bm_path, data)
        print(f"saved + validated: {bm_path}")

if __name__ == "__main__":
    main()
