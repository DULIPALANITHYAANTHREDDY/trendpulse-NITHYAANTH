import requests
import time
import os
import json
from datetime import datetime
BASE_URL = "https://hacker-news.firebaseio.com/v0"
HEADERS = {"User-Agent": "TrendPulse/1.0"}

CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}
def fetch_top_story_ids(limit=500):
    try:
        response = requests.get(f"{BASE_URL}/topstories.json", headers=HEADERS)
        response.raise_for_status()
        return response.json()[:limit]
    except Exception as e:
        print(f"Error fetching top stories: {e}")
        return []
def fetch_story(story_id):
    try:
        response = requests.get(f"{BASE_URL}/item/{story_id}.json", headers=HEADERS)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching story {story_id}: {e}")
        return None
def categorize_story(title):
    if not title:
        return None

    title_lower = title.lower()

    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return None


def extract_fields(story, category):
    return {
        "post_id": story.get("id"),
        "title": story.get("title"),
        "category": category,
        "score": story.get("score", 0),
        "num_comments": story.get("descendants", 0),
        "author": story.get("by"),
        "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

def collect_trending_stories():
    story_ids = fetch_top_story_ids()
    collected = {cat: [] for cat in CATEGORIES.keys()}

    for story_id in story_ids:
        story = fetch_story(story_id)
        if not story:
            continue

        category = categorize_story(story.get("title"))
        if not category:
            continue

        if len(collected[category]) < 25:
            extracted = extract_fields(story, category)
            collected[category].append(extracted)

        # Stop early if all categories filled
        if all(len(v) >= 25 for v in collected.values()):
            break

    # Sleep once per category (as required)
    for _ in CATEGORIES:
        time.sleep(2)

    # Flatten data
    all_stories = []
    for stories in collected.values():
        all_stories.extend(stories)

    return all_stories


# ---------------------------
# Save to JSON
# ---------------------------
def save_to_json(data):
    os.makedirs("data", exist_ok=True)

    filename = datetime.now().strftime("data/trends_%Y%m%d.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

    print(f"Collected {len(data)} stories. Saved to {filename}")
if __name__ == "__main__":
    stories = collect_trending_stories()
    save_to_json(stories)