from kivymd.app import MDApp

from src.ui import UI


class WatcherApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = "Watcher"

    def build(self):
        return UI()


if __name__ == "__main__":
    WatcherApp().run()
