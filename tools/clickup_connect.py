"""
ClickUp Connection Tool
Connects to the ClickUp API and maps the B-Ticket workspace structure.
Usage: python tools/clickup_connect.py
"""

import os
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CLICKUP_API_KEY")
BASE_URL = "https://api.clickup.com/api/v2"


def api_get(endpoint):
    """Make a GET request to the ClickUp API."""
    url = f"{BASE_URL}{endpoint}"
    req = urllib.request.Request(url)
    req.add_header("Authorization", API_KEY)
    req.add_header("Content-Type", "application/json")

    try:
        with urllib.request.urlopen(req) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        print(f"API Error {e.code}: {e.read().decode()}")
        return None


def test_connection():
    """Test API connection and print user info."""
    print("=" * 50)
    print("CLICKUP CONNECTION TEST")
    print("=" * 50)

    # 1. Verify auth
    user_data = api_get("/user")
    if not user_data:
        print("FAILED: Could not authenticate. Check your API key.")
        return False

    user = user_data["user"]
    print(f"Authenticated as: {user['username']} ({user['email']})")
    print()

    # 2. Get teams (workspaces)
    teams_data = api_get("/team")
    if not teams_data or not teams_data.get("teams"):
        print("FAILED: No workspaces found.")
        return False

    # 3. Map workspace structure
    for team in teams_data["teams"]:
        print(f"Workspace: {team['name']} (ID: {team['id']})")
        print("-" * 40)

        # Get spaces
        spaces_data = api_get(f"/team/{team['id']}/space?archived=false")
        if not spaces_data or not spaces_data.get("spaces"):
            print("  No spaces found.")
            continue

        for space in spaces_data["spaces"]:
            print(f"  Space: {space['name']} (ID: {space['id']})")

            # Get folders
            folders_data = api_get(f"/space/{space['id']}/folder?archived=false")
            if folders_data and folders_data.get("folders"):
                for folder in folders_data["folders"]:
                    print(f"    Folder: {folder['name']} (ID: {folder['id']})")
                    for lst in folder.get("lists", []):
                        # Count tasks
                        tasks = api_get(f"/list/{lst['id']}/task?archived=false&page=0")
                        task_count = len(tasks.get("tasks", [])) if tasks else 0
                        print(f"      List: {lst['name']} (ID: {lst['id']}) — {task_count} tasks")

            # Get folderless lists
            lists_data = api_get(f"/space/{space['id']}/list?archived=false")
            if lists_data and lists_data.get("lists"):
                for lst in lists_data["lists"]:
                    tasks = api_get(f"/list/{lst['id']}/task?archived=false&page=0")
                    task_count = len(tasks.get("tasks", [])) if tasks else 0
                    print(f"    List: {lst['name']} (ID: {lst['id']}) — {task_count} tasks")

        print()

    print("=" * 50)
    print("CONNECTION SUCCESSFUL")
    print("=" * 50)
    return True


if __name__ == "__main__":
    if not API_KEY:
        print("ERROR: CLICKUP_API_KEY not found in .env")
    else:
        test_connection()
