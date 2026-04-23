"""
Update ClickUp Docs to match local workflow guides.
Usage: python tools/update_clickup_docs.py
"""

import os
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CLICKUP_API_KEY")
BASE = "https://api.clickup.com/api/v3"
WS = "90161510782"


def update_page(doc_id, page_id, content, name):
    data = json.dumps({"content": content}).encode()
    req = urllib.request.Request(
        f"{BASE}/workspaces/{WS}/docs/{doc_id}/pages/{page_id}",
        data=data, method="PUT"
    )
    req.add_header("Authorization", API_KEY)
    req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"Updated: {name} (status {resp.status})")
    except urllib.error.HTTPError as e:
        print(f"Error updating {name}: {e.code} {e.read().decode()[:200]}")


# === DESIGN DEPARTMENT ===
design_content = """Design Department (Purple)
Folder: B-Ticket
Lists: Design Requests, Merchant Materials, Other (Daimasu, Midori, etc.)

This is your team's workspace for tracking all design work. Everything lives inside one B-Ticket folder.

Your Lists

Design Requests
For all incoming B-Ticket design work - campaign visuals, app mockups, brand materials.

Examples:
- March payday campaign visuals (5 assets)
- New app onboarding screen mockups
- Updated B-Ticket brand guidelines document

Merchant Materials
For merchant-specific collateral - posters, banners, menus for B-Ticket merchants.

Examples:
- Create poster for Jollibee promo
- Design table tent for ABC Restaurant
- Update menu layout for XYZ Cafe

Rule of thumb: If it is for a specific merchant's physical or digital promotion then Merchant Materials. Everything else then Design Requests.

Other (Daimasu, Midori, etc.)
For all design work for the company's other businesses - Daimasu, Midori, and any non-B-Ticket brands.

Examples:
- Daimasu menu update - new seasonal items
- Midori promotional poster - March promo
- Social media assets for Daimasu Instagram

How to Create a Task

Every task must have these fields:

Task name - Be specific: Create poster for Jollibee March promo not just Design poster
Assignee - Which designer is doing the work
Priority - Urgent / High / Normal / Low
Due date - When the requester needs it delivered
Description - What is needed, dimensions/format, brand guidelines, reference images
List - Design Requests, Merchant Materials, or Other (Daimasu, Midori, etc.)

Also Include in the Description:
- Requested by: Which department or person asked for this
- Type: Merchant / Campaign / Brand / Other
- Deliverable format: PNG, PDF, Figma link, etc.
- Dimensions: Social media size, print size, app banner size, etc.

For Multi-Asset Requests use Subtasks:
Task: March payday campaign visuals (5 assets)
  - Facebook banner (1200x628)
  - IG story (1080x1920)
  - IG post (1080x1080)
  - TikTok cover (1080x1920)
  - App banner (750x400)

Statuses - What They Mean for Design

TO DO - Request received, not started yet, sitting in the queue
IN PROGRESS - A designer is actively working on it
REVIEW - Design is done, waiting for the requester's feedback or approval
COMPLETE - Approved and delivered, files sent/uploaded

Move tasks to REVIEW as soon as you send the draft for feedback. Do not wait for approval to move it.

Cross-Department Tags

Use these tags when your task needs something from another department:

needs-marketing - You need campaign details, copy, or a brief before you can start designing
needs-IT - The design needs to be implemented by developers
needs-sales - You need merchant info, photos, or details
blocked - Task is stuck and cannot move forward

When you add a tag, Sheena sees it on her dashboard. She will help coordinate.

Sample Tasks

Task: Create poster for Jollibee promo
List: Merchant Materials (B-Ticket folder) | Priority: High | Due: March 10
Requested by: Sales | Type: Merchant
Deliverable: Print poster (A3) + digital version (1080x1080 for IG)

Task: March payday campaign visuals (5 assets)
List: Design Requests (B-Ticket folder) | Priority: High | Due: March 14
Tags: needs-marketing (need campaign brief)
Subtasks: Facebook banner, IG story, IG post, TikTok cover, App banner

Task: Daimasu menu update - new seasonal items
List: Other (Daimasu, Midori, etc.) | Priority: Normal | Due: March 20
Deliverable: Print menu (A4) + digital version

Your Daily Routine (5 minutes)

1. Open your Design Space then Board View
2. Check TO DO column - any new requests that came in? Do they have enough detail to start?
3. Update statuses - move tasks that progressed
4. Check REVIEW column - anything waiting for feedback for more than 2 days? Follow up
5. Prioritize the backlog - sort TO DO by due date. What is due soonest?
6. Tag missing info - if a request does not have enough detail, add blocked and comment what is missing

Common Mistakes to Avoid

- Requests without a requester name - always note who asked for it and which department
- No due date - every request needs a deadline, even if the requester did not give one (ask them)
- Skipping REVIEW status - do not jump from IN PROGRESS to COMPLETE. REVIEW is where feedback happens
- Not using Merchant Materials list - keep B-Ticket merchant-specific work separate so you can track how many merchants you serve each week
- Mixing lists - B-Ticket design work goes in Design Requests, merchant stuff in Merchant Materials, and Daimasu/Midori work in the Other list. Do not mix them"""


# === MARKETING DEPARTMENT ===
marketing_content = """Marketing Department (Green)
Folder: B-Ticket
Lists: Campaigns, Content Calendar, Paid Ads, Other (Daimasu, Midori, etc.)

This is your team's workspace for tracking all marketing activities. Everything lives inside one B-Ticket folder.

Your Lists

Campaigns
For coordinated marketing pushes with a specific goal, timeframe, and multiple moving parts. Each campaign is one task with subtasks.

Examples:
- March Payday Promo Campaign
- B-Ticket App Launch Push - April
- Valentine's Day Merchant Spotlight Series

Content Calendar - individual content pieces (posts, videos, articles, stories), whether part of a campaign or standalone.

Examples:
- TikTok video - How to redeem coupons
- IG carousel - Top 5 deals this week
- Facebook post - Merchant spotlight: ABC Restaurant

Tip: Use Calendar View for this list - it shows all content plotted on a calendar by due date.

Paid Ads - any marketing where you are spending money (Facebook Ads, Google Ads, Instagram boost, etc.). Tracked separately because it involves budget.

Examples:
- Facebook Ads - App install campaign (PHP 5,000/week)
- Instagram boost - March payday promo post
- Google Ads - coupon app Philippines search campaign

How the 3 B-Ticket Lists Connect:

Campaigns uses content from Content Calendar
Campaigns uses paid promotion from Paid Ads

A campaign like March Payday Promo might have:
- 5 social posts in Content Calendar
- A Facebook ad in Paid Ads
- The campaign task itself in Campaigns (with subtasks linking to these)

But content and ads can also be standalone - not every IG post is part of a campaign.

Other (Daimasu, Midori, etc.)
For all marketing work for the company's other businesses - Daimasu, Midori, and any non-B-Ticket brands.

Examples:
- Daimasu Instagram content - March schedule
- Midori grand opening campaign
- Daimasu Facebook ad - new menu items (PHP 3,000)

How to Create a Task

Every task must have these fields:

Task name - Be specific: TikTok video - How to redeem coupons not just TikTok video
Assignee - Who is creating this content / managing this campaign / running this ad
Priority - Urgent / High / Normal / Low
Due date - Publish date (content), campaign end date, or ad launch date
Description - Brief, target audience, platforms, goals, budget (for ads)
List - Campaigns, Content Calendar, Paid Ads, or Other (Daimasu, Midori, etc.)

For Campaigns use Subtasks:
Task: March Payday Promo Campaign
  - Write campaign brief
  - Create social posts (5 pieces) - needs-design
  - Set up Facebook ad - PHP 3,000 budget
  - Build landing page - needs-IT
  - Schedule push notification - needs-IT
  - Post-campaign report

For Content Calendar Also Include:
- Platform: Facebook, Instagram, TikTok, Twitter/X, Blog
- Content type: Post, story, reel, video, carousel, article
- Publish date: The exact date it goes live

For Paid Ads Also Include:
- Platform: Facebook Ads, Google Ads, Instagram, TikTok Ads
- Budget: Total budget and daily/weekly spend
- Goal: App installs, clicks, impressions, leads
- Run dates: Start and end date

Statuses - What They Mean for Marketing

TO DO - Planned but not started
IN PROGRESS - Actively working - writing copy, creating visuals, setting up ad campaign
REVIEW - Content/ad ready for approval before publishing
COMPLETE - Published, live, or campaign ended

Cross-Department Tags

needs-design - You need visuals, banners, or creative assets
needs-IT - You need a landing page, push notification, app banner, or technical integration
needs-sales - You need merchant info or coordination for merchant-focused content
blocked - Task is stuck

When you add a tag, Sheena sees it on her dashboard. She will help coordinate.

Sample Tasks

Task: March Payday Promo Campaign
List: Campaigns (B-Ticket folder) | Priority: High | Due: March 15-31
Tags: needs-design, needs-IT
Goal: Boost coupon redemptions by 20% during payday period
Budget: PHP 8,000 total

Task: TikTok video - How to redeem coupons
List: Content Calendar (B-Ticket folder) | Priority: Normal | Due: March 10
Platform: TikTok | Type: Tutorial video (30-60 seconds)

Task: Facebook Ads - App install campaign
List: Paid Ads (B-Ticket folder) | Priority: High | Due: March 31
Budget: PHP 5,000/week (PHP 20,000 total for March)
Target: 18-35, Metro Manila, food/dining interests

Task: Daimasu Instagram content - March schedule
List: Other (Daimasu, Midori, etc.) | Priority: Normal | Due: March 31

Using Calendar View

For the Content Calendar list, switch to Calendar View:
1. Open your Marketing Space then Content Calendar list
2. Click + View at the top then select Calendar
3. You will see all content tasks plotted by their due date

Your Daily Routine (5 minutes)

1. Open your Marketing Space then Board View
2. Check Content Calendar - anything publishing today or tomorrow? Is it ready?
3. Check Campaigns - any campaign subtasks due this week? Are they on track?
4. Check Paid Ads - any active ads? Quick check on spend vs budget
5. Update statuses - move tasks as work progresses
6. Tag cross-department needs - if you need design assets or IT help, tag it now

Common Mistakes to Avoid

- Putting everything in Campaigns - standalone content goes in Content Calendar, not Campaigns
- Not tracking ad spend - every peso spent should be in a Paid Ads task with budget and results
- No publish dates on content - the Calendar View only works if every content task has a due date
- Campaign tasks without subtasks - a campaign is multiple activities, break it down
- Mixing lists - B-Ticket campaigns go in Campaigns, content in Content Calendar, ads in Paid Ads, and Daimasu/Midori work in the Other list"""


if __name__ == "__main__":
    print("Updating ClickUp Docs...")
    update_page("2kz0pyby-1076", "2kz0pyby-376", design_content, "Design Department")
    update_page("2kz0pyby-1116", "2kz0pyby-416", marketing_content, "Marketing Department")
    # Sales has no changes, but keeping the doc_id for reference:
    # Sales: doc=2kz0pyby-1096, page=2kz0pyby-396
    print("Sales Department - no changes needed")
    print("\nDone! All ClickUp Docs updated.")
