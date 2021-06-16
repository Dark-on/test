import datetime

from src.db.api import DBApi


class DataProvider:

    DB_NAME = "watcher"

    def __init__(self):
        self.db_api = DBApi(DataProvider.DB_NAME)

    def get_goals(self) -> list[dict]:
        goals = self.db_api.fetchall("goals", ("name", "type", "options"))
        return goals

    def create_goal(self, name, type, options=None):
        if options:
            options = ", ".join(options)
        goal = {
            "name": name,
            "type": type,
            "options": options
        }
        self.db_api.insert("goals", goal)

    def get_records(self, goal) -> list[dict]:
        goal_id = self._get_goal_id(goal)
        records = self.db_api.fetchall(
            "progress",
            ("choice", "note", "date"),
            search_field="goal_id",
            search_value=goal_id
        )
        return records

    def save_progress_record(self, goal:str, choice: str, note: str):
        goal_id = self._get_goal_id(goal)
        record = {
            "date": datetime.date.today(),
            "choice": choice,
            "note": note,
            "goal_id": goal_id
        }
        self.db_api.insert("progress", record)

    def _get_goal_id(self, goal):
        return self.db_api.fetchall(
            "goals",
            ("id",),
            search_field="name",
            search_value=goal
        )[0]["id"]
