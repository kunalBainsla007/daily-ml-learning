#!/usr/bin/env python3
"""
Daily ML Learning Auto-Logger & Streak Tracker
Parses GitHub Issue Form submissions, creates formatted markdown notes in /logs,
calculates learning streaks, and updates the README dashboard.
"""

import os
import sys
import re
import json
from datetime import datetime, date, timedelta, timezone
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parent.parent.parent
LOGS_DIR = REPO_ROOT / "logs"
README_PATH = REPO_ROOT / "README.md"


def clean_field_value(value: str) -> str:
    """Removes GitHub default placeholder for empty optional fields."""
    if not value:
        return ""
    val = value.strip()
    if val in ["_No response_", "None", "N/A", "n/a"]:
        return ""
    return val


def parse_issue_body(body_text: str) -> dict:
    """
    Parses GitHub Issue Form markdown into a dictionary of key-value fields.
    """
    data = {
        "day": "",
        "date": "",
        "topic": "",
        "category": "🧠 Core Machine Learning",
        "summary": "",
        "code": "",
        "resources": "",
        "rating": "⭐⭐⭐⭐⭐ (Crystal Clear)",
        "time_spent": ""
    }

    # Match sections: "### Section Name\n\nContent..."
    sections = re.split(r'(?m)^###\s+', body_text)
    
    for section in sections:
        if not section.strip():
            continue
        lines = section.strip().split("\n", 1)
        header = lines[0].strip().lower()
        content = lines[1].strip() if len(lines) > 1 else ""
        content = clean_field_value(content)

        if "day" in header:
            data["day"] = content
        elif "date" in header:
            data["date"] = content
        elif "topic" in header or "title" in header:
            data["topic"] = content
        elif "category" in header or "domain" in header:
            data["category"] = content
        elif "key concepts" in header or "learnings" in header or "summary" in header:
            data["summary"] = content
        elif "code" in header or "equation" in header:
            data["code"] = content
        elif "resource" in header or "reference" in header:
            data["resources"] = content
        elif "confidence" in header or "rating" in header:
            data["rating"] = content
        elif "time" in header:
            data["time_spent"] = content

    # Fallbacks if parsing had missing fields
    if not data["date"]:
        data["date"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    
    # Clean day number e.g. "Day 1", "01", "1" -> "1"
    day_match = re.search(r'\d+', data["day"])
    if day_match:
        data["day_num"] = int(day_match.group(0))
        data["day_str"] = f"Day {data['day_num']:03d}"
    else:
        # Fallback: estimate day number from existing logs count + 1
        existing_logs = list(LOGS_DIR.glob("*.md"))
        data["day_num"] = len(existing_logs) + 1
        data["day_str"] = f"Day {data['day_num']:03d}"

    if not data["topic"]:
        data["topic"] = "Daily ML Study"

    return data


def slugify(text: str) -> str:
    """Converts a title into a URL & filename safe slug."""
    text = text.lower()
    text = re.sub(r'[^a-z0-9]+', '-', text)
    return text.strip('-')[:50]


def create_log_file(data: dict) -> Path:
    """Generates the Markdown note file in logs/ directory."""
    LOGS_DIR.mkdir(parents=True, exist_ok=True)
    
    slug = slugify(data["topic"])
    filename = f"day-{data['day_num']:03d}_{slug}.md"
    file_path = LOGS_DIR / filename

    code_block = ""
    if data["code"]:
        # If user didn't wrap in backticks, wrap in python markdown fence
        if not data["code"].startswith("```"):
            code_block = f"\n## 💻 Code / Implementation\n```python\n{data['code']}\n```\n"
        else:
            code_block = f"\n## 💻 Code / Implementation\n{data['code']}\n"

    resources_block = ""
    if data["resources"]:
        resources_block = f"\n## 🔗 References & Resources\n{data['resources']}\n"

    rating_str = data["rating"] if data["rating"] else "⭐⭐⭐⭐⭐"
    time_str = data["time_spent"] if data["time_spent"] else "1 hour"

    content = f"""# {data['day_str']}: {data['topic']}

| 📅 Date | 🏷️ Category | ⏱️ Time Spent | ⭐ Rating |
|:---|:---|:---|:---|
| `{data['date']}` | **{data['category']}** | `{time_str}` | {rating_str} |

---

## 💡 Key Learnings & Concepts
{data['summary']}
{code_block}{resources_block}
---
*Logged automatically via [Daily ML Learning Tracker](https://github.com/{os.environ.get('GITHUB_REPOSITORY', 'kunalBainsla007/daily-ml-learning')}) on {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}*
"""

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    return file_path


def parse_all_logs() -> list:
    """
    Parses all markdown files in logs/ to gather statistics and build TOC.
    """
    logs = []
    if not LOGS_DIR.exists():
        return logs

    for file_path in LOGS_DIR.glob("day-*.md"):
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

            # Extract title
            title_match = re.search(r'^#\s+(Day\s+\d+):\s*(.*)$', text, re.MULTILINE)
            day_str = title_match.group(1) if title_match else file_path.stem
            topic = title_match.group(2).strip() if title_match else file_path.stem

            day_num_match = re.search(r'\d+', day_str)
            day_num = int(day_num_match.group(0)) if day_num_match else 0

            # Extract table metadata
            # Row format: | `2026-08-22` | **Category** | `time` | rating |
            table_row_match = re.search(r'\|\s*`(\d{4}-\d{2}-\d{2})`\s*\|\s*\*\*([^*]+)\*\*\s*\|\s*`([^`]*)`\s*\|\s*([^|\n]+)\s*\|', text)
            if table_row_match:
                log_date = table_row_match.group(1).strip()
                category = table_row_match.group(2).strip()
                rating_raw = table_row_match.group(4).strip()
                # Extract stars or rating text
                rating = rating_raw.split('(')[0].strip() if '(' in rating_raw else rating_raw
            else:
                date_match = re.search(r'`(\d{4}-\d{2}-\d{2})`', text)
                log_date = date_match.group(1) if date_match else "2026-01-01"
                cat_match = re.search(r'\*\*([^*]+)\*\*', text)
                category = cat_match.group(1) if cat_match else "Core ML"
                rating = "⭐⭐⭐⭐⭐"

            logs.append({
                "day_num": day_num,
                "day_str": f"Day {day_num:03d}",
                "topic": topic,
                "date": log_date,
                "category": category,
                "rating": rating,
                "file_name": file_path.name,
                "file_path": f"logs/{file_path.name}"
            })
        except Exception as e:
            print(f"Warning: Could not parse {file_path}: {e}")

    logs.sort(key=lambda x: x["day_num"], reverse=True)
    return logs


def calculate_streak(logs: list) -> tuple:
    """Calculates current continuous daily streak and total days."""
    if not logs:
        return 0, 0

    dates = sorted(list(set(l["date"] for l in logs)))
    date_objs = []
    for d in dates:
        try:
            date_objs.append(datetime.strptime(d, "%Y-%m-%d").date())
        except ValueError:
            pass

    if not date_objs:
        return len(logs), len(logs)

    total_days = len(logs)

    # Current streak calculation
    date_set = set(date_objs)
    today = date.today()
    latest_log = date_objs[-1]

    # If the latest log was today or yesterday, streak is alive
    if (today - latest_log).days <= 1:
        current_check = latest_log
        streak = 0
        while current_check in date_set:
            streak += 1
            current_check -= timedelta(days=1)
    else:
        # Streak was broken or latest is earlier
        streak = 1

    return streak, total_days


def generate_table_of_contents(logs: list) -> str:
    """Generates the Markdown Table of Contents for README."""
    if not logs:
        return "*No logs recorded yet. Start logging from your phone! 🚀*"

    table = "| Day | Date | Topic | Domain | Rating | Note |\n"
    table += "|:---|:---|:---|:---|:---:|:---:|\n"

    for l in logs:
        table += f"| **{l['day_str']}** | `{l['date']}` | **{l['topic']}** | {l['category']} | {l['rating']} | [Read Note 📖]({l['file_path']}) |\n"

    return table.strip()


def generate_category_stats(logs: list) -> str:
    """Generates a category breakdown badges list."""
    if not logs:
        return ""

    counts = {}
    for l in logs:
        cat = l["category"]
        counts[cat] = counts.get(cat, 0) + 1

    badges = []
    for cat, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
        badges.append(f"`{cat}: {count} days`")

    return " • ".join(badges)


def update_readme(logs: list, streak: int, total_days: int):
    """Updates dynamic sections in README.md."""
    if not README_PATH.exists():
        print("README.md not found, skipping README update.")
        return

    with open(README_PATH, "r", encoding="utf-8") as f:
        readme = f.read()

    # Badges replacement
    streak_badge = f"![Streak](https://img.shields.io/badge/Current_Streak-{streak}_Days-flame?style=for-the-badge&logo=fire&logoColor=white&color=FF5722)"
    days_badge = f"![Total Days](https://img.shields.io/badge/Total_Logged-{total_days}_Days-blue?style=for-the-badge&logo=target&logoColor=white&color=2196F3)"
    status_badge = f"![Status](https://img.shields.io/badge/Status-Active_Learning-success?style=for-the-badge&color=4CAF50)"

    badges_block = f"{streak_badge} {days_badge} {status_badge}"

    # Replace BADGES section
    if "<!-- BADGES_START -->" in readme and "<!-- BADGES_END -->" in readme:
        readme = re.sub(
            r'<!-- BADGES_START -->.*?<!-- BADGES_END -->',
            f'<!-- BADGES_START -->\n<p align="center">\n  {badges_block}\n</p>\n<!-- BADGES_END -->',
            readme,
            flags=re.DOTALL
        )

    # Replace STATS section
    category_summary = generate_category_stats(logs)
    if "<!-- CATEGORY_STATS_START -->" in readme and "<!-- CATEGORY_STATS_END -->" in readme:
        readme = re.sub(
            r'<!-- CATEGORY_STATS_START -->.*?<!-- CATEGORY_STATS_END -->',
            f'<!-- CATEGORY_STATS_START -->\n{category_summary}\n<!-- CATEGORY_STATS_END -->',
            readme,
            flags=re.DOTALL
        )

    # Replace TABLE OF CONTENTS section
    toc_table = generate_table_of_contents(logs)
    if "<!-- LOG_TABLE_START -->" in readme and "<!-- LOG_TABLE_END -->" in readme:
        readme = re.sub(
            r'<!-- LOG_TABLE_START -->.*?<!-- LOG_TABLE_END -->',
            f'<!-- LOG_TABLE_START -->\n{toc_table}\n<!-- LOG_TABLE_END -->',
            readme,
            flags=re.DOTALL
        )

    with open(README_PATH, "w", encoding="utf-8") as f:
        f.write(readme)

    print("README.md updated successfully.")


def set_github_output(name: str, value: str):
    """Sets output for GitHub Actions workflow steps."""
    output_file = os.environ.get("GITHUB_OUTPUT")
    if output_file:
        with open(output_file, "a", encoding="utf-8") as f:
            f.write(f"{name}={value}\n")


def main():
    # 1. Determine input source
    issue_body = os.environ.get("ISSUE_BODY", "")
    event_path = os.environ.get("GITHUB_EVENT_PATH", "")

    if not issue_body and event_path and os.path.exists(event_path):
        with open(event_path, "r", encoding="utf-8") as f:
            event_data = json.load(f)
            issue_body = event_data.get("issue", {}).get("body", "")

    # For local test / fallback from CLI
    if not issue_body and len(sys.argv) > 1:
        with open(sys.argv[1], "r", encoding="utf-8") as f:
            issue_body = f.read()

    if not issue_body:
        print("No issue body provided. Regenerating README from existing logs...")
        logs = parse_all_logs()
        streak, total_days = calculate_streak(logs)
        update_readme(logs, streak, total_days)
        return

    print("--- Parsing Daily ML Log ---")
    data = parse_issue_body(issue_body)
    print(f"Parsed Day: {data['day_str']}, Topic: {data['topic']}, Date: {data['date']}")

    # 2. Create Note file
    created_file = create_log_file(data)
    print(f"Created log file: {created_file}")

    # 3. Re-parse all logs & update README
    logs = parse_all_logs()
    streak, total_days = calculate_streak(logs)
    update_readme(logs, streak, total_days)

    # 4. Set GitHub Action outputs
    set_github_output("day_str", data["day_str"])
    set_github_output("topic", data["topic"])
    set_github_output("streak", str(streak))
    set_github_output("total_days", str(total_days))
    set_github_output("file_name", created_file.name)
    print(f"Summary: Streak = {streak} days, Total = {total_days} days.")


if __name__ == "__main__":
    main()
