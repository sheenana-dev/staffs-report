"""
Daily department report: fetches tasks from ClickUp (Marketing, Design, Sales)
and sends a summary to Telegram.

- Completed today: tasks whose status.type == "closed" AND date_closed within today (PHT)
- In progress: tasks whose status.type == "custom" (not open, not closed)

Usage:
  python3 tools/daily_report.py           # fetch and send to Telegram
  python3 tools/daily_report.py --dry-run # print report, do not send
"""

import os
import sys
import json
import re
import urllib.request
import urllib.error
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

CLICKUP_API_KEY = os.getenv("CLICKUP_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

CLICKUP_BASE = "https://api.clickup.com/api/v2"
TELEGRAM_BASE = "https://api.telegram.org"

PHT = timezone(timedelta(hours=8))

SPACES = {
    "IT": "90166460444",
    "Marketing": "90166460468",
    "Design": "90166460460",
    "Sales": "90166460463",
    "CS": "90166857552",
}

# Sales is reported per-salesperson, split by ClickUp list: each entry maps a list
# name (exactly as it appears in ClickUp) to the section label shown in the report.
# These are dedicated per-person lists in the Sales space; the Onboarding and Account
# Management lists are intentionally not shown. Run tools/ensure_sales_lists.py to
# create any of these that don't exist yet. To add a person, add a row here.
SALES_LISTS = [
    {"list": "Sales Cei", "label": "Madam Cei"},
    {"list": "Sales Sarah", "label": "Sarah"},
]

# Within each salesperson's list, the report surfaces ONLY these ClickUp statuses,
# in display order — everything else in the list is ignored. Matching is
# case-insensitive on the exact status name. Each status is filtered to the report
# day via `date_field`: only tasks whose that-timestamp falls on the report date are
# shown (the day's activity, not the whole standing pipeline). Set date_field to None
# to show every task currently in the status regardless of date.
#   Contacted  -> date_updated: the lead was worked/moved that day
#   Closed Won -> date_closed:  the deal was closed that day
SALES_STATUSES = [
    {"status": "Contacted", "date_field": "date_updated"},
    {"status": "Closed Won", "date_field": "date_closed"},
]


def clickup_get(endpoint):
    url = f"{CLICKUP_BASE}{endpoint}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", CLICKUP_API_KEY)
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def get_lists_in_space(space_id):
    lists = []
    folders = clickup_get(f"/space/{space_id}/folder?archived=false").get("folders", [])
    for folder in folders:
        for lst in folder.get("lists", []):
            lists.append(lst)
    folderless = clickup_get(f"/space/{space_id}/list?archived=false").get("lists", [])
    lists.extend(folderless)
    return lists


def get_tasks_in_list(list_id):
    tasks = []
    page = 0
    while True:
        data = clickup_get(
            f"/list/{list_id}/task"
            f"?archived=false&include_closed=true&subtasks=true&page={page}"
        )
        batch = data.get("tasks", [])
        tasks.extend(batch)
        if len(batch) < 100:
            break
        page += 1
    return tasks


def report_anchor():
    """Midnight PHT of the report day.

    Uses REPORT_DATE (YYYY-MM-DD) when set by the workflow — it is noon-anchored
    so a late-firing cron that slips past midnight still reports the correct day.
    Falls back to the current PHT day for local/manual runs.
    """
    override = os.getenv("REPORT_DATE")
    if override:
        return datetime.strptime(override, "%Y-%m-%d").replace(tzinfo=PHT)
    return datetime.now(PHT).replace(hour=0, minute=0, second=0, microsecond=0)


def pht_today_bounds(anchor):
    start = anchor.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=1)
    return int(start.timestamp() * 1000), int(end.timestamp() * 1000)


def classify(task, today_start_ms, today_end_ms):
    status = task.get("status", {}) or {}
    stype = status.get("type", "")
    date_closed = task.get("date_closed")
    if stype == "closed" and date_closed:
        try:
            closed_ms = int(date_closed)
            if today_start_ms <= closed_ms < today_end_ms:
                return "completed_today"
        except (ValueError, TypeError):
            pass
    if stype == "custom":
        return "in_progress"
    return None


def clean_name(name):
    # Collapse all whitespace (incl. embedded newlines from ClickUp) into single
    # spaces. Newlines inside a name would let the 4096-char chunk splitter cut
    # mid-<a> tag, producing malformed HTML that Telegram rejects with HTTP 400.
    return " ".join((name or "").split()) or "(unnamed)"


def task_entry(task, list_name):
    assignees = ", ".join(
        a.get("username", "?") for a in task.get("assignees", [])
    ) or "unassigned"
    return {
        "name": clean_name(task.get("name")),
        "url": task.get("url", ""),
        "status": (task.get("status") or {}).get("status", ""),
        "list": list_name,
        "assignees": assignees,
    }


def collect_department_report(dept_name, space_id, today_start_ms, today_end_ms):
    completed = []
    in_progress = []
    for lst in get_lists_in_space(space_id):
        try:
            tasks = get_tasks_in_list(lst["id"])
        except urllib.error.HTTPError:
            continue
        for task in tasks:
            bucket = classify(task, today_start_ms, today_end_ms)
            if bucket is None:
                continue
            entry = task_entry(task, lst["name"])
            if bucket == "completed_today":
                completed.append(entry)
            else:
                in_progress.append(entry)
    return {"completed": completed, "in_progress": in_progress}


def escape_html(s):
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def sales_status_match(task, status_cfg, today_start_ms, today_end_ms):
    name = ((task.get("status") or {}).get("status") or "").strip().lower()
    if name != status_cfg["status"].strip().lower():
        return False
    date_field = status_cfg.get("date_field")
    if not date_field:
        return True  # no date filter — show all tasks currently in this status
    try:
        ts = int(task.get(date_field))
    except (ValueError, TypeError):
        return False
    return today_start_ms <= ts < today_end_ms


def collect_sales_sections(space_id, today_start_ms, today_end_ms):
    """One section per salesperson (matched by ClickUp list name), each showing
    only the configured statuses (Contacted, Closed Won) as separate buckets.
    Unmapped lists (Onboarding, Account Management) and other statuses are excluded."""
    def norm(s):
        return (s or "").strip().lower()

    label_for = {norm(m["list"]): m["label"] for m in SALES_LISTS}
    buckets = {
        m["label"]: {s["status"]: [] for s in SALES_STATUSES} for m in SALES_LISTS
    }
    for lst in get_lists_in_space(space_id):
        label = label_for.get(norm(lst["name"]))
        if label is None:
            continue
        try:
            tasks = get_tasks_in_list(lst["id"])
        except urllib.error.HTTPError:
            continue
        for task in tasks:
            for status_cfg in SALES_STATUSES:
                if sales_status_match(task, status_cfg, today_start_ms, today_end_ms):
                    buckets[label][status_cfg["status"]].append(
                        task_entry(task, lst["name"])
                    )
                    break
    return [
        (
            f"Sales — {m['label']}",
            [
                {
                    "label": s["status"],
                    "entries": buckets[m["label"]][s["status"]],
                    "cap": 20,
                }
                for s in SALES_STATUSES
            ],
        )
        for m in SALES_LISTS
    ]


def render_task_lines(entries, cap=None):
    lines = []
    for t in (entries if cap is None else entries[:cap]):
        name = escape_html(t["name"])
        lines.append(f"• <a href=\"{t['url']}\">{name}</a>" if t["url"] else f"• {name}")
    if cap is not None and len(entries) > cap:
        lines.append(f"  <i>… +{len(entries) - cap} more</i>")
    return lines


def render_section(title, buckets):
    lines = [f"<b>{title}</b>"]
    for bucket in buckets:
        entries = bucket["entries"]
        lines.append(f"{bucket['label']} ({len(entries)})")
        lines += render_task_lines(entries, cap=bucket.get("cap")) if entries else ["  <i>None</i>"]
    lines.append("")
    return lines


def standard_buckets(data):
    return [
        {"label": "Completed", "entries": data["completed"], "cap": None},
        {"label": "In progress", "entries": data["in_progress"], "cap": 20},
    ]


def build_sections(report_by_dept, sales_sections):
    sections = [
        ("Marketing", standard_buckets(report_by_dept["Marketing"])),
        ("Design", standard_buckets(report_by_dept["Design"])),
    ]
    sections += sales_sections
    sections.append(("CS", standard_buckets(report_by_dept["CS"])))
    return sections


def format_report(report_by_dept, sales_sections, date_str):
    lines = [f"<b>Daily Report — {date_str}</b>", ""]
    for title, buckets in build_sections(report_by_dept, sales_sections):
        lines += render_section(title, buckets)
    return "\n".join(lines).strip()


def chunk_message(text, limit=4096):
    chunks = []
    remaining = text
    while len(remaining) > limit:
        split_at = remaining.rfind("\n", 0, limit)
        if split_at == -1:
            split_at = limit
        chunks.append(remaining[:split_at])
        remaining = remaining[split_at:].lstrip("\n")
    if remaining:
        chunks.append(remaining)
    return chunks


def html_to_plain(html):
    """Best-effort plain-text version of a chunk: links collapse to their text,
    bold/italic markers drop, and entities unescape. Used as a fallback when
    Telegram rejects the HTML so the report still gets delivered."""
    text = re.sub(r'<a\s+href="[^"]*">(.*?)</a>', r"\1", html)
    text = re.sub(r"</?[bi]>", "", text)
    return text.replace("&lt;", "<").replace("&gt;", ">").replace("&amp;", "&")


def telegram_post(url, chunk, parse_mode):
    """POST one chunk. Returns None on success, or Telegram's error description
    (read from the response body — that's the actual reason for a 400)."""
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": chunk,
        "disable_web_page_preview": True,
    }
    if parse_mode:
        payload["parse_mode"] = parse_mode
    req = urllib.request.Request(url, data=json.dumps(payload).encode(), method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read().decode())
        return None if body.get("ok") else body.get("description", str(body))
    except urllib.error.HTTPError as e:
        try:
            return json.loads(e.read().decode()).get("description", f"HTTP {e.code}")
        except (ValueError, OSError):
            return f"HTTP {e.code}"


def send_telegram(text):
    url = f"{TELEGRAM_BASE}/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    for chunk in chunk_message(text):
        err = telegram_post(url, chunk, parse_mode="HTML")
        if err is None:
            continue
        # Surface the real reason, then retry the chunk as plain text so a single
        # formatting edge case never blocks the whole report (and the run marker).
        print(f"⚠️  Telegram rejected HTML chunk ({err}) — retrying as plain text")
        err2 = telegram_post(url, html_to_plain(chunk), parse_mode=None)
        if err2 is not None:
            raise RuntimeError(
                f"Telegram send failed — HTML: {err}; plain-text fallback: {err2}"
            )


def main():
    dry_run = "--dry-run" in sys.argv

    # A dry-run only fetches from ClickUp and prints — it never sends, so it does
    # not need the Telegram credentials.
    required = {"CLICKUP_API_KEY": CLICKUP_API_KEY}
    if not dry_run:
        required["TELEGRAM_BOT_TOKEN"] = TELEGRAM_BOT_TOKEN
        required["TELEGRAM_CHAT_ID"] = TELEGRAM_CHAT_ID
    missing = [k for k, v in required.items() if not v]
    if missing:
        print(f"ERROR: missing env vars: {', '.join(missing)}")
        sys.exit(1)

    anchor = report_anchor()
    today_start_ms, today_end_ms = pht_today_bounds(anchor)
    today_str = anchor.strftime("%a, %b %d, %Y")

    report = {}
    for dept, space_id in SPACES.items():
        if dept == "Sales":
            continue  # collected separately, per salesperson + status
        print(f"Collecting {dept} ...")
        report[dept] = collect_department_report(
            dept, space_id, today_start_ms, today_end_ms
        )

    print("Collecting Sales (per salesperson) ...")
    sales_sections = collect_sales_sections(
        SPACES["Sales"], today_start_ms, today_end_ms
    )

    text = format_report(report, sales_sections, today_str)
    print("\n" + "=" * 60)
    print(text)
    print("=" * 60 + "\n")

    if dry_run:
        print("(dry-run — not sending)")
        return

    send_telegram(text)
    print("Sent to Telegram ✅")


if __name__ == "__main__":
    main()
