# reads snapchat json

import json

def load_memories(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    items = data.get("Saved Media", [])
    memories = []

    for item in items:
        if not item.get("Media Download Url"):
            continue

        memories.append({
            "url": item["Media Download Url"],
            "date": item.get("Date"),
            "type": item.get("Media Type").lower()
        })

    return memories