from utils.database import (
    add_newcomer, add_message, add_alert,
    create_initial_tasks, get_db
)
from datetime import datetime, timedelta

print("Loading demo data...")

# 1. Create 5 newcomers
newcomers = [
    {"name": "Alexey Ivanov", "position": "Senior Developer", "department": "Engineering", 
     "start_date": (datetime.now() - timedelta(days=14)).strftime('%Y-%m-%d'), "mentor": "Dmitry Petrov",
     "mood": [5,5,4,5,5], "chat": "positive"},
    {"name": "Maria Sidorova", "position": "Product Manager", "department": "Product",
     "start_date": (datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d'), "mentor": "Elena Sokolova",
     "mood": [4,4,5,5,5], "chat": "curious"},
    {"name": "Dmitry Kuznetsov", "position": "Sales Manager", "department": "Sales",
     "start_date": (datetime.now() - timedelta(days=3)).strftime('%Y-%m-%d'), "mentor": "Olga Morozova",
     "mood": [4,3,2,2,1], "chat": "negative"},
    {"name": "Elena Volkova", "position": "Marketing Specialist", "department": "Marketing",
     "start_date": (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d'), "mentor": "Igor Novikov",
     "mood": [3,4], "chat": "neutral"},
    {"name": "Sergey Popov", "position": "Support Engineer", "department": "Support",
     "start_date": (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d'), "mentor": "Anna Lebedeva",
     "mood": [3,3,3], "chat": "minimal"}
]

created = []
for nc in newcomers:
    nid = add_newcomer(nc["name"], nc["position"], nc["department"], nc["start_date"], nc["mentor"])
    if nid:
        print(f"OK: {nc['name']} ({nid})")
        created.append({**nc, "id": nid})

# 2. Chat messages
chats = {
    "positive": [("Hi!", "Great! Team is friendly"), ("How days?", "Love onboarding"), ("Questions?", "Want to know tools")],
    "curious": [("Hi!", "Good but lots new"), ("Studying?", "Product architecture"), ("Mentor?", "Very helpful")],
    "negative": [("Hi!", "Hard... lots to learn"), ("Worried?", "Feel behind, too fast"), ("Help?", "Need more support")],
    "neutral": [("Hi!", "OK, adjusting"), ("Questions?", "None yet")],
    "minimal": [("Hi!", "OK"), ("Questions?", "No")]
}

for nc in created:
    msgs = chats.get(nc["chat"], chats["neutral"])
    for u, b in msgs:
        add_message(nc["id"], u, "user")
        add_message(nc["id"], b, "buddy")
    print(f"  Chat: {len(msgs)} msgs for {nc['name']}")

# 3. Mood tracking
for nc in created:
    for i, m in enumerate(nc["mood"]):
        fb = "Good day" if m >= 4 else "OK" if m == 3 else "Hard"
        conn = get_db()
        conn.execute("INSERT INTO mood_checkins (newcomer_id, mood_score, feedback) VALUES (?,?,?)",
                    (nc["id"], m, fb))
        conn.commit()
        conn.close()
    print(f"  Mood: {len(nc['mood'])} entries for {nc['name']}")

# 4. Alerts
alerts = [
    (created[2]["id"], "high", "Low mood (1/5) + negative chat"),
    (created[2]["id"], "medium", "Mood drop: 4->1 in 3 days"),
    (created[4]["id"], "low", "Low activity (10 days)")
]
for aid, level, reason in alerts:
    add_alert(aid, level, reason)
    print(f"  Alert: {reason}")

# 5. Tasks
for nc in created[:3]:
    create_initial_tasks(nc["id"])
    print(f"  Tasks: 5 starter for {nc['name']}")

print("\nDemo data loaded!")
print(f"  - {len(created)} newcomers")
print(f"  - Chats filled")
print(f"  - Mood tracked")
print(f"  - Alerts created")
print(f"  - Tasks assigned")
print("\nOpen http://localhost:8501/hr to see filled dashboard!")
