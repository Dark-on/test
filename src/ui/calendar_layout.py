import calendar
from datetime import date

from kivy.lang import Builder
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout

from src.data_provider import dpr
from config import Config


Builder.load_file(f"{Config.TEMPLATES_DIR}/calendar_layout.kv")


class CalendarCell(MDBoxLayout):
    def __init__(self, text, color, halign="center", valign="center", **kwargs):
        super().__init__(**kwargs)
        self.md_bg_color = color
        self.add_widget(
            MDLabel(
                text=str(text),
                markup=True,
                halign=halign,
                valign=valign,
                padding=(5, 5)
            )
        )


class CalendarLayout(MDGridLayout):

    def __init__(self, **kwargs):
        super().__init__(cols=7, rows=7, **kwargs)
        self._offset = 0

    def load_content(self, goal):
        self.clear_widgets()

        self.goal = goal
        calendar_matrix = self._get_calendar()
        week_days = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")

        for day_name in week_days:
            self.add_widget(
                CalendarCell(
                    text=day_name,
                    color=(0.75, 0.61, 0.84, 1)
                )
            )
        for week in calendar_matrix:
            for day_number in week:
                day_number = "" if day_number == 0 else day_number
                color, choice = self._get_day_color_and_choice(day_number)
                self.add_widget(
                    CalendarCell(
                        text=f"{day_number}\n[b]{choice}[/b]",
                        color=color,
                        halign="left",
                        valign="top"
                    )
                )

    def _get_day_color_and_choice(self, day):
        records = dpr.get_records(self.goal.get("name"))
        color = (1, 1, 1, 0)
        choice = ""
        for record in records:
            if record.get("date") == f"{self.year}-{self.month:02}-{day}":
                color = (0.58, 0.82, 0.56, 1)
                choice = record.get("choice") if record.get("choice") else "Note"
                break
        return color, choice

    def next_month(self):
        self._offset += 1
        self.load_content(self.goal)

    def previous_month(self):
        self._offset -= 1
        self.load_content(self.goal)

    def _get_calendar(self):
        current_date = date.today()
        self.month = current_date.month - 1 + self._offset
        self.year = current_date.year + self.month // 12
        self.month = self.month % 12 + 1
        return calendar.monthcalendar(self.year, self.month)
