from re import S
from kivy.core import text
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
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

from src.data_provider import DataProvider
from config import Config
from src.data_provider import dp

class GoalsTab(MDBottomNavigationItem):

    def __init__(self, **kwargs):
        super().__init__(name="goals", text="goals",
                         icon="note-plus", **kwargs)
        self.scroll_view = ScrollView(do_scroll_y=True, effect_cls='ScrollEffect')
        self.layout = MDBoxLayout(orientation="vertical", size_hint=(1, 1.1))
        self.load_content()
        self.scroll_view.add_widget(self.layout)
        self.add_widget(self.scroll_view)

    def load_content(self):
        self.layout.clear_widgets()

        goals_list = dp.get_goals()

        toolbar = MDToolbar(type="top")
        toolbar.left_action_items = [["arrow-left", self.go_back]]
        toolbar.right_action_items = [["plus", self.add_goal]]

        for goal in goals_list:
            name_label = MDLabel(
                text=goal["name"],
                halign="left",
                valign="top",
            )

        type_label = MDLabel(
            text="Тип поля вводу: ",
            halign="left",
            valign="top",
        )
        options_label = MDLabel(
            text="Варіанти: ",
            halign="left",
            valign="top",
        )
        self.is_need_fild = False

        # dropdown = DropDown()
        # items = ("Вибір з варіантів", "Нотатка")
        # for item in items:
        #     btn = Button(text=item, size_hint_y=None, height=2)
        #     btn.bind(on_release=lambda btn: dropdown.select(btn.text))
        #     dropdown.add_widget(btn)
        # self.mainbutton = Button(text='Оберіть (тиць)', size_hint=(0.8, 0.5))
        # self.mainbutton.bind(on_release=dropdown.open)
        # dropdown.bind(on_select=self.select_text)

        variants_label = MDLabel(text="Вибір з варіантів")
        notes_label = MDLabel(text="Нотатка")
        variants_checkbox = MDCheckbox(group="1", on_press=self.variants_func)
        notes_checkbox = MDCheckbox(group="1", on_press=self.notes_func)

        self.name_input = MDTextField()
        self.options_input = MDTextField()

        self.layout.add_widget(toolbar)
        self.layout.add_widget(name_label)
        self.layout.add_widget(self.name_input)
        self.layout.add_widget(type_label)

        self.layout.add_widget(variants_label)
        self.layout.add_widget(variants_checkbox)
        self.layout.add_widget(notes_label)
        self.layout.add_widget(notes_checkbox)
        self.layout.add_widget(options_label)
        # self.layout.add_widget(self.mainbutton)
        self.layout.add_widget(self.options_input)


    # def select_text(self, instance, x):
    #     # self.is_need_fild = True if x == "Вибір з варіантів" else False
    #     self.mainbutton.text = x

    def variants_func(self, instance):
        self.type_goal="options"

    def notes_func(self, instance):
        self.type_goal="notes"

    # def set_item(self, text__item):
    #     self.type_input.dismiss()

    def go_back(self, touch):
        self.layout.clear_widgets()
        self.manager.transition.direction = "right"
        self.manager.switch_to(GoalsTab.screens["goals_list"])

    def add_goal(self, touch):
        dp.create_goal(self.name_input.text, self.type_goal, options=list(self.options_input.text.split(" ")))
        goals_list = dp.get_goals()
        GoalsTab.screens["goals_list"].load_goals_list(goals_list)
        self.go_back(touch)
