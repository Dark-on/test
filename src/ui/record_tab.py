from re import S
from kivy.core import text
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import ILeftBody, MDList, ThreeLineListItem
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.list import OneLineIconListItem
from kivy.uix.scrollview import ScrollView
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from datetime import date

from src.data_provider import DataProvider
from config import Config
from src.data_provider import dpr

from kivymd.uix.menu import MDDropdownMenu
from  kivymd.uix.dropdownitem import MDDropDownItem


class IconListItem(OneLineIconListItem):
    icon = StringProperty()


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
            name_label = MDLabel(
                text=goal["name"],
                theme_text_color="Custom",
                text_color=(0, 1, 0, 1),
                halign="left",
                valign="top",
            )
            self.layout.add_widget(name_label)
            checkbox_list = []
            if goal["type"] == "notes":
                note = MDTextField()
                self.layout.add_widget(note)
                self.notes_input.append(note)
            else:
                for option in goal["options"]:
                    goal_label = MDLabel(text=option)
                    goal_checkbox = MDCheckbox(group=goal["name"], on_press=self.variants_func)
                    self.layout.add_widget(goal_label)
                    self.layout.add_widget(goal_checkbox)
                    checkbox_list.append(goal_checkbox)
                    self.notes_input.append(None)
            self.checkbox_lists.append(checkbox_list)

    def set_item(self, item):
         self.menu.dismiss()
         self.dropdown_item.set_item(item)

        # variants_label = MDLabel(text="Вибір з варіантів")
        # notes_label = MDLabel(text="Нотатка")
        # variants_checkbox = MDCheckbox(group="1", on_press=self.variants_func)
        # notes_checkbox = MDCheckbox(group="1", on_press=self.notes_func)

    def select_text(self, instance, x):
        self.mainbutton.text = x

    def variants_func(self, instance):
        pass

    def notes_func(self, instance):
        self.type_goal="notes"

    def add_record(self, touch):
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
