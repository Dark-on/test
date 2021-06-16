import kivy

from kivy.app import App

from kivy.uix.dropdown import DropDown
from kivy.uix.button import Button
from kivy.lang import Builder

Builder.load_string("""

<CustomDropDown>

""")

class CustomDropDown(DropDown):

    def __init__(self, items=("First", "Second", "Third", "Fourth"), **kwargs):
        super().__init__(**kwargs)

        for item in items:
            self.add_widget(Button(text=item, size_hint_y=None, height=44, on_release=self.my_select(item)))

    def my_select(self, item):
        return lambda x: self.select(item)


class MyApp(App):
    def build(self):

        mainbutton = Button(text = "Select Item",
                            size_hint = (0.5, 0.1),
                            pos_hint = {'center_x':0.5, 'center_y':0.5})
        dropdown = CustomDropDown()

        mainbutton.bind(on_release = dropdown.open)
        dropdown.bind(on_select = lambda instance, x: setattr(mainbutton, "text", x))
        return mainbutton

if __name__ == "__main__":
    MyApp().run()