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
    "Marketing": "90166460468",
    "Design": "90166460460",
    "Sales": "90166460463",
}


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


def pht_today_bounds():
    now_pht = datetime.now(PHT)
    start = now_pht.replace(hour=0, minute=0, second=0, microsecond=0)
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


def collect_department_report(dept_name, space_id, today_start_ms, today_end_ms):
    completed = []
    in_progress = []
    lists = get_lists_in_space(space_id)
    for lst in lists:
        try:
            tasks = get_tasks_in_list(lst["id"])
        except urllib.error.HTTPError:
            continue
        for task in tasks:
            bucket = classify(task, today_start_ms, today_end_ms)
            if bucket is None:
                continue
            assignees = ", ".join(
                a.get("username", "?") for a in task.get("assignees", [])
            ) or "unassigned"
            entry = {
                "name": task.get("name", "(unnamed)"),
                "url": task.get("url", ""),
                "status": (task.get("status") or {}).get("status", ""),
                "list": lst["name"],
                "assignees": assignees,
            }
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


def format_report(report_by_dept, date_str):
    lines = [f"<b>📊 Daily Report — {date_str}</b>", ""]
    for dept in ["Marketing", "Design", "Sales"]:
        data = report_by_dept[dept]
        lines.append(f"<b>━━━ {dept} ━━━</b>")

        lines.append(f"<b>✅ Completed today ({len(data['completed'])})</b>")
        if data["completed"]:
            for t in data["completed"]:
                name = escape_html(t["name"])
                lst = escape_html(t["list"])
                if t["url"]:
                    lines.append(f"• <a href=\"{t['url']}\">{name}</a> — {lst}")
                else:
                    lines.append(f"• {name} — {lst}")
        else:
            lines.append("  <i>None</i>")

        lines.append("")
        lines.append(f"<b>🔄 In progress ({len(data['in_progress'])})</b>")
        if data["in_progress"]:
            for t in data["in_progress"][:20]:
                name = escape_html(t["name"])
                lst = escape_html(t["list"])
                if t["url"]:
                    lines.append(f"• <a href=\"{t['url']}\">{name}</a> — {lst}")
                else:
                    lines.append(f"• {name} — {lst}")
            if len(data["in_progress"]) > 20:
                lines.append(f"  <i>… +{len(data['in_progress']) - 20} more</i>")
        else:
            lines.append("  <i>None</i>")

        lines.append("")
    return "\n".join(lines).strip()


def send_telegram(text):
    url = f"{TELEGRAM_BASE}/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    chunks = []
    remaining = text
    limit = 4000
    while len(remaining) > limit:
        split_at = remaining.rfind("\n", 0, limit)
        if split_at == -1:
            split_at = limit
        chunks.append(remaining[:split_at])
        remaining = remaining[split_at:].lstrip("\n")
    if remaining:
        chunks.append(remaining)

    for chunk in chunks:
        payload = json.dumps({
            "chat_id": TELEGRAM_CHAT_ID,
            "text": chunk,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }).encode()
        req = urllib.request.Request(url, data=payload, method="POST")
        req.add_header("Content-Type", "application/json")
        with urllib.request.urlopen(req) as resp:
            body = json.loads(resp.read().decode())
            if not body.get("ok"):
                raise RuntimeError(f"Telegram error: {body}")


def main():
    dry_run = "--dry-run" in sys.argv

    missing = [k for k, v in {
        "CLICKUP_API_KEY": CLICKUP_API_KEY,
        "TELEGRAM_BOT_TOKEN": TELEGRAM_BOT_TOKEN,
        "TELEGRAM_CHAT_ID": TELEGRAM_CHAT_ID,
    }.items() if not v]
    if missing:
        print(f"ERROR: missing env vars: {', '.join(missing)}")
        sys.exit(1)

    today_start_ms, today_end_ms = pht_today_bounds()
    today_str = datetime.now(PHT).strftime("%a, %b %d, %Y")

    report = {}
    for dept, space_id in SPACES.items():
        print(f"Collecting {dept} ...")
        report[dept] = collect_department_report(
            dept, space_id, today_start_ms, today_end_ms
        )

    text = format_report(report, today_str)
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
