from re import S
from kivy.core import text
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.uix.image import AsyncImage
from kivy.properties import StringProperty
from kivy.metrics import dp
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import ILeftBody, MDList, ThreeLineAvatarListItem
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.list import OneLineIconListItem
from kivy.uix.scrollview import ScrollView
from kivymd.uix.selectioncontrol import MDCheckbox
from kivy.lang import Builder

from src.data_provider import DataProvider
from config import Config


Builder.load_file(f"{Config.TEMPLATES_DIR}/goalstab.kv")
dp = DataProvider()

class IconListItem(OneLineIconListItem):
    icon = StringProperty()


class AsyncImageLeftWidget(ILeftBody, AsyncImage):
    pass


class GoalCreatorScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.scroll_view = ScrollView(do_scroll_y=True, effect_cls='ScrollEffect')
        self.layout = MDBoxLayout(orientation="vertical", size_hint=(1, 1.1))
        self.load_content()
        self.scroll_view.add_widget(self.layout)
        self.add_widget(self.scroll_view)

    def load_content(self):
        self.layout.clear_widgets()

        toolbar = MDToolbar(type="top")
        toolbar.left_action_items = [["arrow-left", self.go_back]]
        toolbar.right_action_items = [["plus", self.add_goal]]

        name_label = MDLabel(
            text="Назва цілі: ",
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
        # goal = Goal(
        #     title=self.title_input.text,
        #     vote_average=self.vote_input.text,
        # )
        # GoalsTab.screens["goals_list"].goals.append(goal)
        # goals_list = GoalsTab.screens["goals_list"].goals
        # GoalsTab.screens["goals_list"].load_goals_list(goals_list)
        self.go_back(touch)


class GoalInfoContent(MDBoxLayout):

    def __init__(self, goal, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        text_info = (
            f"[color=#707070]Id:[/color] {goal.id_}\n"
            f"[color=#707070]Title:[/color] {goal.title}\n"
            f"[color=#707070]Vote average:[/color] {goal.vote_average}\n\n"
            f"[color=#707070]Overview:[/color] {goal.details.overview}\n"
            f"[color=#707070]Tagline:[/color] {goal.details.tagline}\n"
            f"[color=#707070]Status:[/color] {goal.details.status}\n"
            f"[color=#707070]Genres:[/color] {goal.details.genres}\n"
        )
        # cover = AsyncImage(source=goal.poster_path, size_hint_y=0.4)
        info = MDLabel(
            text=text_info,
            markup=True,
            halign="left",
            valign="top",
            size_hint_y=1
        )

        # self.add_widget(cover)
        self.add_widget(info)


class CalendarScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll_view = ScrollView()
        self.layout = MDBoxLayout(orientation="vertical", size_hint=(1, 1.2))
        scroll_view.add_widget(self.layout)
        self.add_widget(scroll_view)

    def load_screen(self, goal):
        self.goal = goal

        toolbar = MDToolbar(type="top")
        toolbar.left_action_items = [["arrow-left", self.go_back]]
        toolbar.right_action_items = [["delete", self.delete_item]]

        content = (goal)

        self.layout.add_widget(toolbar)
        self.layout.add_widget(content)

    def go_back(self, touch):
        self.layout.clear_widgets()
        self.manager.transition.direction = "right"
        self.manager.switch_to(GoalsTab.screens["goals_list"])

    def delete_item(self, touch):
        GoalsTab.screens["goals_list"].goals.remove(self.goal)
        goals_list = GoalsTab.screens["goals_list"].goals
        GoalsTab.screens["goals_list"].load_goals_list(goals_list)
        self.go_back(touch)


class GoalListItem(ThreeLineAvatarListItem):
    """List item with the cover and short information about the goal."""

    def __init__(self, goal, **kwargs):
        super().__init__(text=goal["name"],
                         secondary_text=goal["type"],
                         tertiary_text=f"Options: {' '.join(goal['options'])}",
                         **kwargs)
        self.goal = goal

        # image = AsyncImageLeftWidget(source=self.goal.poster_path)

        # self.add_widget(image)

    def on_release(self):
        GoalsTab.screens["calendar"].load_screen(self.goal)
        GoalsTab.screen_manager.transition.direction = "left"
        GoalsTab.screen_manager.switch_to(GoalsTab.screens["calendar"])


class GoalsListScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.goals = []

        add_goal_button = MDFloatingActionButton(
            icon="plus",
            on_release=self.open_goal_creator_screen
        )

        self.layout = MDBoxLayout(orientation="vertical")

        self.scroll_view = ScrollView()
        self.layout.add_widget(self.scroll_view)

        self.add_widget(self.layout)
        self.add_widget(add_goal_button)

    def load_goals_list(self, goals):
        self.scroll_view.clear_widgets()

        self.goals = goals
        mdlist = MDList()

        for goal in self.goals:
            list_item_widget = GoalListItem(goal)
            mdlist.add_widget(list_item_widget)

        self.scroll_view.add_widget(mdlist)

    def open_goal_creator_screen(self, touch):
        GoalsTab.screens["goal_creator"].load_content()
        GoalsTab.screen_manager.transition.direction = "left"
        GoalsTab.screen_manager.switch_to(GoalsTab.screens["goal_creator"])


class GoalsTab(MDBottomNavigationItem):

    screen_manager = None
    screens = None

    def __init__(self, **kwargs):
        super().__init__(name="goals", text="goals",
                         icon="note-plus", **kwargs)

        GoalsTab.screen_manager = ScreenManager()
        GoalsTab.screens = {
            "goals_list": GoalsListScreen(name="goals_list"),
            "goal_creator": GoalCreatorScreen(name="goal_creator"),
            "calendar": CalendarScreen(name="calendar")
        }

        for screen in self.screens.values():
            GoalsTab.screen_manager.add_widget(screen)

        self.add_widget(GoalsTab.screen_manager)
