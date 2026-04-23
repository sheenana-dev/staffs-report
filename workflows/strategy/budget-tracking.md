# Budget Tracking

## Purpose
Keep spending visible and controlled across all departments. You don't need to be a finance expert — you need to know where money is going, whether it's being spent wisely, and when to flag concerns.

## When
- Set budgets at the start of each quarter (during quarterly planning)
- Track monthly during the monthly review
- Review individual expenses as they come up (approval workflow)

## Steps

### Step 1: Understand Your Budget Categories

Each department has recurring and variable costs:

**IT Department**
- Server / hosting costs (AWS, GCP, etc.)
- Software licenses and subscriptions
- App store developer fees
- Third-party API costs (SMS, email, maps, payment gateway)
- Equipment (laptops, monitors)

**Design Department**
- Design tool subscriptions (Figma, Adobe, etc.)
- Stock assets (photos, icons, fonts)
- Printing costs (merchant materials)
- Equipment

**Sales Department**
- Transportation / field allowances
- Client meals and entertainment
- Sales tools / CRM subscription
- Promotional materials (samples, brochures)
- Commission / incentives

**Marketing Department**
- Paid advertising (Facebook Ads, Google Ads, TikTok Ads)
- Influencer partnerships
- Content creation costs (photography, video)
- Events and activations
- Social media tools

### Step 2: Set Monthly Budget Per Department

Use this simple format:

| Department | Monthly Budget | Notes |
|-----------|---------------|-------|
| IT | PHP [amount] | Mostly fixed costs |
| Design | PHP [amount] | Mostly fixed costs |
| Sales | PHP [amount] | Variable — scales with activity |
| Marketing | PHP [amount] | Variable — scales with campaigns |
| **Total** | **PHP [amount]** | |

**Rule of thumb for startups:**
- IT + Design = 40-50% of budget (product is the business)
- Sales = 20-25% (growth engine)
- Marketing = 25-35% (user acquisition)

Adjust based on B-Ticket's current priorities.

### Step 3: Approval Workflow

| Amount | Who Approves |
|--------|-------------|
| Under PHP 5,000 | Department lead |
| PHP 5,000 - 25,000 | You (Sheena) |
| Over PHP 25,000 | You + company leadership |
| Unbudgeted expenses | Always you |

### Step 4: Track Monthly

Create a simple Google Sheet:

```
Columns:
A: Date
B: Department
C: Category (from Step 1)
D: Description
E: Amount (PHP)
F: Budgeted? (Yes/No)
G: Approved by
H: Receipt/proof (link)

Summary tab:
- Budget vs actual per department
- % of budget used (month-to-date)
- Projected month-end spend
```

### Step 5: Monthly Review

During the monthly review, check:
1. Is each department within budget?
2. Any unexpected expenses?
3. Is the spending producing results? (tie back to KPIs)
4. Any upcoming large expenses to plan for?

## Templates

### Google Sheet: Monthly Budget Tracker
```
B-TICKET MONTHLY BUDGET - [Month] [Year]

| Department | Budget | Spent | Remaining | % Used |
|-----------|--------|-------|-----------|--------|
| IT | PHP X | PHP X | PHP X | X% |
| Design | PHP X | PHP X | PHP X | X% |
| Sales | PHP X | PHP X | PHP X | X% |
| Marketing | PHP X | PHP X | PHP X | X% |
| TOTAL | PHP X | PHP X | PHP X | X% |

Status:
- Green: Under 80% at this point in the month
- Yellow: 80-100%
- Red: Over budget
```

### Telegram: Budget Approval Request Format
```
BUDGET REQUEST

From: [department]
What: [clear description of the expense]
Amount: PHP [amount]
Category: [from the category list]
Budgeted: [Yes — it was planned / No — it's unplanned]
Why: [business reason]
Timing: [when do we need to pay]

@Sheena for approval
```

### Telegram: Monthly Budget Update
```
Budget Update - [Month]

IT: PHP [spent] / PHP [budget] — [X]% used [status]
Design: PHP [spent] / PHP [budget] — [X]% used [status]
Sales: PHP [spent] / PHP [budget] — [X]% used [status]
Marketing: PHP [spent] / PHP [budget] — [X]% used [status]

Total: PHP [spent] / PHP [budget] — [X]% used

Notable items:
- [Any large or unusual expenses]

Forecast: [on track / will exceed by X]
```

### Telegram: Expense Reminder to Leads
```
Monthly reminder to all leads:

Please submit all expense receipts and requests by [date — 3 days before month end].

Format:
- Date | Description | Amount | Category | Receipt photo

Send to the budget sheet: [link]
Late submissions will be counted in next month's budget.
```

## Red Flags
- Department consistently over budget — either the budget is wrong or spending is uncontrolled
- No receipts or documentation — hard to track and audit
- Marketing spending doesn't correlate with results — money going in, nothing coming out
- Unbudgeted expenses every month — planning is weak
- Budget approval process is bypassed — "I already paid for it" is not okay
- No one knows the budget amounts — leads need to see their numbers

## Cost-Saving Tips for B-Ticket
- **IT:** Use free tiers where possible (many cloud services have startup programs)
- **Design:** Figma has free plans for small teams; use open-source icon libraries
- **Sales:** Track cost per merchant acquired — if it's too high, fix the process before spending more
- **Marketing:** Start with organic content before paid ads; micro-influencers cost less than big names
- **All:** Review subscriptions quarterly — cancel anything unused for 2+ months
