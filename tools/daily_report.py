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
# day via `date_fields`: only tasks whose timestamp falls on the report date are
# shown (the day's activity, not the whole standing pipeline). Set date_fields to
# None to show every task currently in the status regardless of date.
#   Contacted  -> date_updated: the lead was worked/moved that day
#   Closed Won -> date_closed:  the deal was closed that day
# date_fields is tried in order; the first one ClickUp has populated dates the
# task. Closed Won needs the date_updated fallback because ClickUp only sets
# date_closed for statuses whose *type* is "closed" — and status types are
# per-list. A list that configures Closed Won as a custom-type status leaves
# date_closed null forever, which silently drops every closed deal from the
# report while an identically-named status on another list keeps working.
SALES_STATUSES = [
    {"status": "Contacted", "date_fields": ("date_updated",)},
    {"status": "Closed Won", "date_fields": ("date_closed", "date_updated")},
]


def warn(msg):
    """Surface a problem in the run log without failing the run. An empty section
    is otherwise indistinguishable from a genuinely quiet day — that ambiguity hid
    a blank Sales section for nine weekdays in Aug 2026 before anyone noticed."""
    print(f"⚠️  {msg}")


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
        except urllib.error.HTTPError as e:
            warn(f"{dept_name}: skipped list '{lst['name']}' ({lst['id']}) — HTTP {e.code}")
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


def task_timestamp(task, date_fields):
    """First populated timestamp among date_fields, in epoch ms. None if the task
    carries none of them — an unset field is null, not absent, so this cannot be
    a plain task.get()."""
    for field in date_fields:
        try:
            return int(task.get(field))
        except (ValueError, TypeError):
            continue
    return None


def in_status(task, status_cfg):
    name = ((task.get("status") or {}).get("status") or "").strip().lower()
    return name == status_cfg["status"].strip().lower()


def sales_status_match(task, status_cfg, today_start_ms, today_end_ms):
    if not in_status(task, status_cfg):
        return False
    date_fields = status_cfg.get("date_fields")
    if not date_fields:
        return True  # no date filter — show all tasks currently in this status
    ts = task_timestamp(task, date_fields)
    if ts is None:
        return False
    return today_start_ms <= ts < today_end_ms


def status_breakdown(tasks):
    """Count tasks by their current ClickUp status name, most common first."""
    seen = {}
    for task in tasks:
        name = ((task.get("status") or {}).get("status") or "?").strip() or "?"
        seen[name] = seen.get(name, 0) + 1
    return sorted(seen.items(), key=lambda kv: (-kv[1], kv[0]))


def last_activity_pht(tasks, status_cfg):
    """Newest report-relevant timestamp among tasks currently in status_cfg, as a
    PHT string. Distinguishes 'wrong status' from 'right status, wrong day'."""
    date_fields = status_cfg.get("date_fields")
    if not date_fields:
        return None
    stamps = [
        ts
        for task in tasks
        if in_status(task, status_cfg)
        for ts in [task_timestamp(task, date_fields)]
        if ts is not None
    ]
    if not stamps:
        return None
    newest = datetime.fromtimestamp(max(stamps) / 1000, PHT)
    return f"{newest:%Y-%m-%d %H:%M} PHT"


def explain_empty_section(label, tasks):
    """Say why a salesperson's section came out empty, so a status rename or a
    lead parked in an unreported status is visible in the log instead of looking
    like a quiet day."""
    if not tasks:
        warn(f"Sales — {label}: list has 0 tasks.")
        return
    breakdown = ", ".join(f"{n} ({c})" for n, c in status_breakdown(tasks))
    wanted = ", ".join(s["status"] for s in SALES_STATUSES)
    warn(
        f"Sales — {label}: none of {len(tasks)} tasks matched [{wanted}] for the "
        f"report day. Statuses present: {breakdown}"
    )
    for status_cfg in SALES_STATUSES:
        seen_at = last_activity_pht(tasks, status_cfg)
        if seen_at:
            warn(
                f"Sales — {label}: newest '{status_cfg['status']}' activity by "
                f"{'/'.join(status_cfg['date_fields'])} was {seen_at} — outside "
                f"the report day."
            )


def match_list_tasks(lst, today_start_ms, today_end_ms):
    """Bucket one salesperson list's tasks by reported status.
    Returns (buckets_by_status, all_tasks)."""
    tasks = get_tasks_in_list(lst["id"])
    matches = {s["status"]: [] for s in SALES_STATUSES}
    for task in tasks:
        for status_cfg in SALES_STATUSES:
            if sales_status_match(task, status_cfg, today_start_ms, today_end_ms):
                matches[status_cfg["status"]].append(task_entry(task, lst["name"]))
                break
    return matches, tasks


def warn_unresolved_lists(matched_lists):
    """A configured salesperson whose list never turned up in the Sales space —
    renamed or deleted — otherwise reports as a permanently quiet day."""
    for mapping in SALES_LISTS:
        if mapping["label"] not in matched_lists:
            warn(
                f"Sales — {mapping['label']}: no list named '{mapping['list']}' in the "
                f"Sales space — renamed or deleted? Section will be empty."
            )


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
    matched_lists, unmapped = {}, []
    for lst in get_lists_in_space(space_id):
        label = label_for.get(norm(lst["name"]))
        if label is None:
            unmapped.append(f"'{lst['name']}' ({lst['id']})")
            continue
        where = f"'{lst['name']}' ({lst['id']})"
        matched_lists[label] = where
        try:
            matches, tasks = match_list_tasks(lst, today_start_ms, today_end_ms)
        except urllib.error.HTTPError as e:
            warn(f"Sales — {label}: skipped list {where} — HTTP {e.code}")
            continue
        buckets[label] = matches
        found = sum(len(v) for v in matches.values())
        print(f"  Sales — {label}: list {where}, {len(tasks)} tasks, {found} reportable")
        if not found:
            explain_empty_section(label, tasks)
    warn_unresolved_lists(matched_lists)
    if unmapped:
        print(f"  Sales: ignored unmapped lists — {', '.join(unmapped)}")
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


def telegram_post(url, chat_id, chunk, parse_mode):
    """POST one chunk to chat_id. Returns (ok, description, migrate_to_chat_id).
    description is Telegram's real error text (from the response body);
    migrate_to_chat_id is set when the group was upgraded to a supergroup."""
    payload = {
        "chat_id": chat_id,
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
    except urllib.error.HTTPError as e:
        try:
            body = json.loads(e.read().decode())
        except (ValueError, OSError):
            return (False, f"HTTP {e.code}", None)
    if body.get("ok"):
        return (True, None, None)
    migrate = (body.get("parameters") or {}).get("migrate_to_chat_id")
    return (False, body.get("description", str(body)), migrate)


def send_telegram(text):
    url = f"{TELEGRAM_BASE}/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    chat_id = TELEGRAM_CHAT_ID
    for chunk in chunk_message(text):
        ok, desc, migrate = telegram_post(url, chat_id, chunk, "HTML")
        if not ok and migrate:
            # Group was upgraded to a supergroup, so its id changed. Follow the new
            # id for the rest of the run and log it so the TELEGRAM_CHAT_ID secret
            # can be updated (which removes this extra round-trip next time).
            print(f"ℹ️  Group upgraded to supergroup — new chat_id={migrate}. "
                  f"Update the TELEGRAM_CHAT_ID secret to {migrate}.")
            chat_id = str(migrate)
            ok, desc, _ = telegram_post(url, chat_id, chunk, "HTML")
        if ok:
            continue
        # Not a migration — surface the reason and retry as plain text so a
        # formatting edge case never blocks the whole report (and the run marker).
        print(f"⚠️  Telegram rejected HTML chunk ({desc}) — retrying as plain text")
        ok, desc2, _ = telegram_post(url, chat_id, html_to_plain(chunk), None)
        if not ok:
            raise RuntimeError(
                f"Telegram send failed — HTML: {desc}; plain-text fallback: {desc2}"
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
