from src.db.api import DBApi
from src.data_provider import dpr


api = DBApi("watcher")
api.insert("goals", {"name": "Mood", "type": "notes", "options": None})
api.insert("goals", {"name": "Run", "type": "options", "options": "Easy, Medium, Hard"})
api.insert("goals", {"name": "Restfulness", "type": "options", "options": "Yes, No"})
print(dpr.get_goals())
api.insert(
    "progress",
    {
        "date": "2021-05-28",
        "choice": None,
        "notes": "Feeling good",
        "goal_id": 1
    }
)
api.insert(
    "progress",
    {
        "date": "2021-06-03",
        "choice": None,
        "notes": "Feeling good",
        "goal_id": 1
    }
)
api.insert(
    "progress",
    {
        "date": "2021-06-05",
        "choice": None,
        "notes": "Feeling bad, I don't know why",
        "goal_id": 1
    }
)
api.insert(
    "progress",
    {
        "date": "2021-06-07",
        "choice": "Easy",
        "notes": None,
        "goal_id": 2
    }
)
api.insert(
    "progress",
    {
        "date": "2021-06-08",
        "choice": "Hard",
        "notes": None,
        "goal_id": 2
    }
)
api.insert(
    "progress",
    {
        "date": "2021-06-16",
        "choice": "Yes",
        "notes": None,
        "goal_id": 3
    }
)
api.insert(
    "progress",
    {
        "date": "2021-06-17",
        "choice": "No",
        "notes": None,
        "goal_id": 3
    }
)
print(dpr.get_records("Mood"))
print(dpr.get_records("Run"))
print(dpr.get_records("Restfulness"))
