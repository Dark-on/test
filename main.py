from kivymd.app import MDApp

from src.db.api import DBApi
from src.ui import UI


class Lab3App(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Drozd Svitlana IV-81"

    def build(self):
        return UI()


if __name__ == "__main__":
    db_api = DBApi("watcher")
    db_api.create_db()
    db_api.insert("goals", {"name": "run"})
    Lab3App().run()
