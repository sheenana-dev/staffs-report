"""
Ensure each configured Sales list exists in the ClickUp Sales space.

Idempotent and safe to re-run. For each per-person list in SALES_LISTS
(daily_report.py):
  - if it already exists            -> skip
  - if it's the target of a RENAME  -> rename the existing source list to it
                                       (preserves that list's tasks)
  - otherwise                       -> create a new folderless list

RENAMES lets an existing lifecycle list become a per-person list without losing
its tasks (e.g. "Merchant Leads" -> "Sales Cei", where Madam Cei's leads already
live). Requires CLICKUP_API_KEY in a local .env (this repo has no local .env by
default; the key otherwise lives only in GitHub Actions).

Usage:
  python3 tools/ensure_sales_lists.py --dry-run  # show what would change
  python3 tools/ensure_sales_lists.py            # apply
"""

import os
import sys
import json
import urllib.request
from dotenv import load_dotenv

# Reuse config + the read helper from the report tool (single source of truth).
from daily_report import SPACES, SALES_LISTS, get_lists_in_space

load_dotenv()

CLICKUP_API_KEY = os.getenv("CLICKUP_API_KEY")
CLICKUP_BASE = "https://api.clickup.com/api/v2"

# existing ClickUp list name -> new per-person name. The source is renamed in place,
# so its tasks carry over instead of being stranded in a now-unread list.
RENAMES = {
    "Merchant Leads": "Sales Cei",  # Madam Cei's existing leads already live here
}


def norm(name):
    return (name or "").strip().lower()


def list_id_by_name(space_id):
    return {norm(lst["name"]): lst["id"] for lst in get_lists_in_space(space_id)}


def _write(method, url, name):
    payload = json.dumps({"name": name}).encode()
    req = urllib.request.Request(url, data=payload, method=method)
    req.add_header("Authorization", CLICKUP_API_KEY)
    req.add_header("Content-Type", "application/json")
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def create_folderless_list(space_id, name):
    return _write("POST", f"{CLICKUP_BASE}/space/{space_id}/list", name)


def rename_list(list_id, new_name):
    return _write("PUT", f"{CLICKUP_BASE}/list/{list_id}", new_name)


def main():
    dry_run = "--dry-run" in sys.argv

    if not CLICKUP_API_KEY:
        print("ERROR: CLICKUP_API_KEY missing — add it to a local .env")
        sys.exit(1)

    space_id = SPACES["Sales"]
    by_name = list_id_by_name(space_id)
    target_to_source = {norm(new): src for src, new in RENAMES.items()}

    for entry in SALES_LISTS:
        name = entry["list"]
        if norm(name) in by_name:
            print(f"✓ exists, skipping: {name}")
            continue

        source = target_to_source.get(norm(name))
        if source and norm(source) in by_name:
            if dry_run:
                print(f"~ would rename: {source} -> {name}")
            else:
                rename_list(by_name[norm(source)], name)
                print(f"~ renamed: {source} -> {name}")
            continue

        if dry_run:
            print(f"+ would create: {name}")
        else:
            created = create_folderless_list(space_id, name)
            print(f"+ created: {created.get('name', name)} (id {created.get('id')})")

    if dry_run:
        print("(dry-run — no changes made)")


if __name__ == "__main__":
    main()
