from os import name
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivy.uix.scrollview import ScrollView
from kivymd.uix.selectioncontrol import MDCheckbox
from datetime import date

from src.data_provider import dpr

class RecordTab(MDBottomNavigationItem):

    def __init__(self, **kwargs):
        super().__init__(name="record", text="record",
                         icon="note-minus", **kwargs)
        self.scroll_view = ScrollView(do_scroll_y=True, effect_cls='ScrollEffect')
        self.layout = MDBoxLayout(orientation="vertical", size_hint=(1, 1.5))
        self.load_content()
        self.scroll_view.add_widget(self.layout)
        self.add_widget(self.scroll_view)

    def load_content(self):
        self.layout.clear_widgets()

        self.goals_list = dpr.get_goals()

        toolbar = MDToolbar(type="top")
        toolbar.title = str(date.today())
        toolbar.right_action_items = [["plus", self.add_record]]
        self.layout.add_widget(toolbar)

        self.notes_input = []
        self.checkbox_lists = []
        for goal in self.goals_list:
            name = goal["name"]
            type_ = goal["type"]
            options = goal["options"]
            name_label = MDLabel(
                text=name,
                theme_text_color="Custom",
                text_color=(0, 1, 0, 1),
                font_style='H6',
                halign="left",
                valign="top",
                padding_x="40"
            )
            self.layout.add_widget(name_label)

            checkbox_list = []
            if type_ == "notes":
                note = MDTextField()
                self.layout.add_widget(note)
                self.notes_input.append(note)
            else:
                for option in options:
                    layout = MDBoxLayout()
                    goal_label = MDLabel(text=option, padding_x="20")
                    goal_checkbox = MDCheckbox(group=name, on_press=self.checkbox_func, pos_hint={'center_x': .4, 'center_y': .5})
                    layout.add_widget(goal_label)
                    layout.add_widget(goal_checkbox)
                    checkbox_list.append(goal_checkbox)
                    self.notes_input.append(None)
                    self.layout.add_widget(layout)
            self.checkbox_lists.append(checkbox_list)

    def checkbox_func(self, instance):
        pass

    def add_record(self):
        for i in range(len(self.goals_list)):
            name = self.goals_list[i]["name"]
            type_ = self.goals_list[i]["type"]
            options = self.goals_list[i]["options"]

            if type_ == "notes":
                dpr.save_progress_record(
                    goal=name,
                    choice=None,
                    notes=self.notes_input[i].text)
            else:
                for j in range(len(options)):
                    if self.checkbox_lists[i][j].active:
                        choise = options[j]
                        break
                dpr.save_progress_record(
                    goal=name,
                    choice=choise,
                    notes=None)

        # goals_list = dpr.get_goals()
        # GoalsTab.screens["goals_list"].load_goals_list(goals_list)
        # self.go_back(touch)
