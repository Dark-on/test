import datetime
from typing import Optional
from sqlite3 import IntegrityError

from src.db.api import DBApi


class DataProvider:

    DB_NAME = "watcher"

    def __init__(self):
        self.db_api = DBApi(DataProvider.DB_NAME)

    def get_goals(self) -> list[dict]:
        goals = self.db_api.fetchall("goals", ("name", "type", "options"))
        for goal in goals:
            options = goal.get("options")
            if options:
                goal["options"] = options.split(", ")
        return goals

    def create_goal(self, name, type, options=None):
        if options:
            options = ", ".join(options)

        if type not in ("options", "notes"):
            return False

        if type == "notes":
            options = None

        goal = {
            "name": name,
            "type": type,
            "options": options
        }
        try:
            self.db_api.insert("goals", goal)
        except IntegrityError:
            return False
        return True

    def get_records(self, goal) -> list[dict]:
        goal_id = self._get_goal_id(goal)
        records = self.db_api.fetchall(
            "progress",
            ("choice", "notes", "date"),
            search_field="goal_id",
            search_value=goal_id
        )
        return records

    def save_progress_record(
            self,
            goal: str,
            choice: Optional[str] = None,
            notes: Optional[str] = None) -> bool:
        if not any((choice, notes)):
            return False

        goal_id = self._get_goal_id(goal)
        record = {
            "date": datetime.date.today(),
            "choice": choice,
            "notes": notes,
            "goal_id": goal_id
        }
        try:
            self.db_api.insert("progress", record)
        except IntegrityError:
            return False
        return True

    def _get_goal_id(self, goal):
        return self.db_api.fetchall(
            "goals",
            ("id",),
            search_field="name",
            search_value=goal
        )[0]["id"]

dpr = DataProvider()
