from kivymd.app import MDApp

from src.ui import UI
from src.data_provider import DataProvider


class WatcherApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Watcher"

    def build(self):
        return UI()


if __name__ == "__main__":
    dp = DataProvider()
    # dp.create_goal("write", "notes")
    # dp.create_goal("run", "options", ["easy", "hard"])
    # dp.save_progress_record("write", choice="", notes="fuck you")
    # dp.save_progress_record("run", choice="easy", notes="")
    # print(dp.get_goals())
    # print(dp.get_records("run"))
    # print(dp.get_records("write"))
    WatcherApp().run()
