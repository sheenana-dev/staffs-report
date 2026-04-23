"""
Blocked Task Alerts
Scans all ClickUp department spaces for tasks tagged 'blocked',
then sends a summary to Telegram DM.
Usage: python tools/blocked_alerts.py
"""

import os
import json
import urllib.request
import urllib.error
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

CLICKUP_API_KEY = os.getenv("CLICKUP_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
CLICKUP_BASE = "https://api.clickup.com/api/v2"
TELEGRAM_BASE = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}"

DEPARTMENT_SPACES = {
    "IT Department": "90166460444",
    "Design Department": "90166460460",
    "Sales Department": "90166460463",
    "Marketing Department": "90166460468",
}


def clickup_get(endpoint):
    """GET request to ClickUp API."""
    req = urllib.request.Request(f"{CLICKUP_BASE}{endpoint}")
    req.add_header("Authorization", CLICKUP_API_KEY)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"ClickUp API Error {e.code}: {e.read().decode()}")
        return None


def send_telegram(message):
    """Send a message via Telegram bot."""
    data = json.dumps({
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown",
    }).encode()
    req = urllib.request.Request(f"{TELEGRAM_BASE}/sendMessage", data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"Telegram Error {e.code}: {e.read().decode()}")
        return None


def get_blocked_tasks():
    """Fetch all tasks tagged 'blocked' across department spaces."""
    blocked = {}

    for dept_name, space_id in DEPARTMENT_SPACES.items():
        dept_blocked = []

        # Get all lists in the space
        lists_data = clickup_get(f"/space/{space_id}/list?archived=false")
        if not lists_data:
            continue

        for lst in lists_data.get("lists", []):
            # Get tasks with 'blocked' tag
            tasks_data = clickup_get(
                f"/list/{lst['id']}/task?archived=false&tags[]=blocked&page=0"
            )
            if not tasks_data:
                continue

            for task in tasks_data.get("tasks", []):
                assignees = ", ".join(
                    [a["username"] for a in task.get("assignees", [])]
                ) or "Unassigned"

                due = "No due date"
                if task.get("due_date"):
                    due_ts = int(task["due_date"]) / 1000
                    due_dt = datetime.fromtimestamp(due_ts)
                    due = due_dt.strftime("%b %d")
                    if due_dt < datetime.now():
                        due += " ⚠️ OVERDUE"

                dept_blocked.append({
                    "name": task["name"],
                    "assignee": assignees,
                    "due": due,
                    "list": lst["name"],
                    "url": task.get("url", ""),
                })

        # Also check folders
        folders_data = clickup_get(f"/space/{space_id}/folder?archived=false")
        if folders_data:
            for folder in folders_data.get("folders", []):
                for lst in folder.get("lists", []):
                    tasks_data = clickup_get(
                        f"/list/{lst['id']}/task?archived=false&tags[]=blocked&page=0"
                    )
                    if not tasks_data:
                        continue
                    for task in tasks_data.get("tasks", []):
                        assignees = ", ".join(
                            [a["username"] for a in task.get("assignees", [])]
                        ) or "Unassigned"
                        due = "No due date"
                        if task.get("due_date"):
                            due_ts = int(task["due_date"]) / 1000
                            due_dt = datetime.fromtimestamp(due_ts)
                            due = due_dt.strftime("%b %d")
                            if due_dt < datetime.now():
                                due += " ⚠️ OVERDUE"
                        dept_blocked.append({
                            "name": task["name"],
                            "assignee": assignees,
                            "due": due,
                            "list": lst["name"],
                            "url": task.get("url", ""),
                        })

        if dept_blocked:
            blocked[dept_name] = dept_blocked

    return blocked


def format_message(blocked):
    """Format blocked tasks into a Telegram message."""
    today = datetime.now().strftime("%B %d, %Y")

    if not blocked:
        return f"✅ *Blocked Task Check — {today}*\n\nNo blocked tasks across any department. All clear!"

    total = sum(len(tasks) for tasks in blocked.values())
    lines = [f"🚨 *Blocked Task Alert — {today}*\n"]
    lines.append(f"*{total} blocked task(s)* found:\n")

    for dept, tasks in blocked.items():
        lines.append(f"*{dept}* ({len(tasks)}):")
        for t in tasks:
            lines.append(f"  • {t['name']}")
            lines.append(f"    Assignee: {t['assignee']} | Due: {t['due']}")
            lines.append(f"    List: {t['list']}")
            if t["url"]:
                lines.append(f"    [Open in ClickUp]({t['url']})")
        lines.append("")

    lines.append("_Action: Follow up with the assignee or their lead today._")
    return "\n".join(lines)


def main():
    print("Scanning ClickUp for blocked tasks...")
    blocked = get_blocked_tasks()

    message = format_message(blocked)
    print("\n--- Message Preview ---")
    print(message)
    print("--- End Preview ---\n")

    print("Sending to Telegram...")
    result = send_telegram(message)
    if result and result.get("ok"):
        print("Sent successfully!")
    else:
        print("Failed to send.")


if __name__ == "__main__":
    main()
