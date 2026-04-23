"""
Add "Task Date" custom field (date type) to target ClickUp Lists.
Usage: python3 tools/clickup_add_task_date.py

Note: ClickUp API creates the field but does NOT support setting required=true.
The "Required" flag must be toggled manually in the ClickUp UI per field.
"""

import os
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CLICKUP_API_KEY")
BASE_URL = "https://api.clickup.com/api/v2"

TARGET_LISTS = [
    ("Marketing → General Operation", "901613801562"),
    ("Marketing → Campaigns", "901613798331"),
    ("Marketing → Content Calendar", "901613798332"),
    ("Marketing → Paid Ads", "901613798333"),
    ("Marketing → Other (Daimasu, Midori, etc.)", "901613799911"),
    ("Design → Design Requests", "901613798327"),
    ("Design → Merchant Materials", "901613798328"),
    ("Design → Other (Daimasu, Midori, etc.)", "901613799910"),
    ("Design → Mancom Report → List", "901613919945"),
    ("Design → B-ticket Magazine → List", "901614033854"),
    ("Design → Creative Dept Attendance → List", "901614611363"),
    ("Sales → Merchant Leads", "901613791022"),
    ("Sales → Onboarding", "901613791027"),
    ("Sales → Account Management", "901613791029"),
    ("IT → Current Development", "901613790988"),
]


def api_request(method, endpoint, payload=None):
    url = f"{BASE_URL}{endpoint}"
    data = json.dumps(payload).encode() if payload else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", API_KEY)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            return resp.status, json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode()


def field_exists(list_id, field_name):
    status, body = api_request("GET", f"/list/{list_id}/field")
    if status != 200:
        return False
    for f in body.get("fields", []):
        if f.get("name", "").lower() == field_name.lower():
            return True
    return False


def main():
    created = []
    skipped = []
    failed = []

    for label, list_id in TARGET_LISTS:
        print(f"Processing: {label}")
        if field_exists(list_id, "Task Date"):
            print(f"  SKIP — 'Task Date' already exists")
            skipped.append(label)
            continue

        status, body = api_request(
            "POST",
            f"/list/{list_id}/field",
            {"name": "Task Date", "type": "date"},
        )
        if status == 200:
            print(f"  CREATED — field id: {body['field']['id']}")
            created.append(label)
        else:
            print(f"  FAILED ({status}): {body}")
            failed.append((label, status, body))

    print()
    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Created: {len(created)}")
    for c in created:
        print(f"  - {c}")
    print(f"Skipped (already exists): {len(skipped)}")
    for s in skipped:
        print(f"  - {s}")
    print(f"Failed: {len(failed)}")
    for f in failed:
        print(f"  - {f}")


if __name__ == "__main__":
    if not API_KEY:
        print("ERROR: CLICKUP_API_KEY not found in .env")
    else:
        main()
