from kivy.uix.screenmanager import ScreenManager
from kivy.uix.scrollview import ScrollView
from kivy.lang import Builder
from kivy.uix.image import AsyncImage
from kivymd.uix.label import MDLabel
from kivymd.uix.screen import MDScreen
from kivymd.uix.list import ILeftBody, MDList, ThreeLineAvatarListItem
# from kivymd.uix.list import ImageLeftWidget
from kivymd.uix.toolbar import MDToolbar
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDFloatingActionButton
from kivymd.uix.bottomnavigation import MDBottomNavigationItem
from kivymd.uix.spinner import MDSpinner

from src.movies_provider import Movie, MoviesProvider
from config import Config


Builder.load_file(f"{Config.TEMPLATES_DIR}/moviestab.kv")


class AsyncImageLeftWidget(ILeftBody, AsyncImage):
    pass


class MovieAdderScreen(MDScreen):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.layout = MDBoxLayout(orientation="vertical")
        self.load_content()

        self.add_widget(self.layout)

    def load_content(self):
        self.layout.clear_widgets()

        toolbar = MDToolbar(type="top")
        toolbar.left_action_items = [["arrow-left", self.go_back]]
        toolbar.right_action_items = [["plus", self.add_movie]]

        id_label = MDLabel(
            text="Id: ",
            halign="left",
            valign="top",
        )
        title_label = MDLabel(
            text="Title: ",
            halign="left",
            valign="top",
        )
        vote_label = MDLabel(
            text="Vote average: ",
            halign="left",
            valign="top",
        )

        self.id_input = MDTextField()
        self.title_input = MDTextField()
        self.vote_input = MDTextField()

        self.layout.add_widget(toolbar)
        self.layout.add_widget(id_label)
        self.layout.add_widget(self.id_input)
        self.layout.add_widget(title_label)
        self.layout.add_widget(self.title_input)
        self.layout.add_widget(vote_label)
        self.layout.add_widget(self.vote_input)

    def go_back(self, touch):
        self.layout.clear_widgets()
        self.manager.transition.direction = "right"
        self.manager.switch_to(MoviesTab.screens["movies_list"])

    def add_movie(self, touch):
        movie = Movie(
            title=self.title_input.text,
            vote_average=self.vote_input.text,
        )
        MoviesTab.screens["movies_list"].movies.append(movie)
        movies_list = MoviesTab.screens["movies_list"].movies
        MoviesTab.screens["movies_list"].load_movies_list(movies_list)
        self.go_back(touch)

class MovieInfoContent(MDBoxLayout):

    def __init__(self, movie, **kwargs):
        super().__init__(orientation="vertical", **kwargs)
        # Create big string with all information about movie.
        text_info = (
            f"[color=#707070]Id:[/color] {movie.id_}\n"
            f"[color=#707070]Title:[/color] {movie.title}\n"
            f"[color=#707070]Vote average:[/color] {movie.vote_average}\n\n"
            f"[color=#707070]Overview:[/color] {movie.details.overview}\n"
            f"[color=#707070]Tagline:[/color] {movie.details.tagline}\n"
            f"[color=#707070]Status:[/color] {movie.details.status}\n"
            f"[color=#707070]Genres:[/color] {movie.details.genres}\n"
        )
        # Create cover of the movie
        cover = AsyncImage(source=movie.poster_path, size_hint_y=0.4)
        # Create label with text_info previously created.
        info = MDLabel(
            text=text_info,
            markup=True,
            halign="left",
            valign="top",
            size_hint_y=1
        )

        # Add movie cover and detailed information to the layout
        self.add_widget(cover)
        self.add_widget(info)


class MovieInfoScreen(MDScreen):
    """Contains layout with detailed information about the choosen
    movie.

    Also containstoolbar with buttons for getting back to the movies list
    and deleting the choosen movie from the list.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        scroll_view = ScrollView()
        self.layout = MDBoxLayout(orientation="vertical", size_hint=(1, 1.2))
        scroll_view.add_widget(self.layout)
        self.add_widget(scroll_view)

    def load_screen(self, movie):
        """Loads all elements for the detailed info.

        Created as separate method because on every movie we need to reload the
        information.
        """
        self.movie = movie

        toolbar = MDToolbar(type="top")
        toolbar.left_action_items = [["arrow-left", self.go_back]]
        toolbar.right_action_items = [["delete", self.delete_item]]

        content = MovieInfoContent(movie)

        self.layout.add_widget(toolbar)
        self.layout.add_widget(content)

    def go_back(self, touch):
        self.layout.clear_widgets()
        self.manager.transition.direction = "right"
        self.manager.switch_to(MoviesTab.screens["movies_list"])

    def delete_item(self, touch):
        MoviesTab.screens["movies_list"].movies.remove(self.movie)
        movies_list = MoviesTab.screens["movies_list"].movies
        MoviesTab.screens["movies_list"].load_movies_list(movies_list)
        self.go_back(touch)


class MovieListItem(ThreeLineAvatarListItem):
    """List item with the cover and short information about the movie."""

    def __init__(self, movie, **kwargs):
        super().__init__(text=movie.title,
                         secondary_text=str(movie.id_),
                         tertiary_text=f"Vote average: {movie.vote_average}",
                         **kwargs)
        self.movie = movie

        image = AsyncImageLeftWidget(source=self.movie.poster_path)

        self.add_widget(image)

    def on_release(self):
        """Called when the user taps on the item and releases it"""
        MoviesTab.screens["movie_info"].load_screen(self.movie)
        MoviesTab.screen_manager.transition.direction = "left"
        MoviesTab.screen_manager.switch_to(MoviesTab.screens["movie_info"])


class SearchField(MDTextField):
    """Input field that is used for searching movies."""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._is_first_run = True

    def make_search(self):
        """Called when user types some text."""
        # Need to skip this method for the first time, because without this
        # skip here will be an error. The first call happens on initialization
        # and not all fields are created for referencing.
        if self._is_first_run:
            self._is_first_run = False
            return
        found_movies = MoviesProvider.find_movies(self.text)
        # Reloading movies list on the screen with new filtered movies
        MoviesTab.screens["movies_list"].load_movies_list(found_movies)


class MoviesListScreen(MDScreen):
    """Screen, contains  the list of movies with short information and the
    search bar.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # In this small block, movies are generated from the json file.
        # (from the task)
        self.movies = []

        add_movie_button = MDFloatingActionButton(
            icon="plus",
            on_release=self.open_movie_adder_screen
        )

        # Creating layout where all inner parts will be placed
        # (such as the foundation of the house)
        self.layout = MDBoxLayout(orientation="vertical")

        self.search_field = SearchField()
        self.spinner = MDSpinner(
            pos_hint={'center_x': .5, 'center_y': .5},
            size_hint=(0.03, 0.03)
        )
        self.spinner.active = False
        # ScrollView allows to scroll list that was put inside of whis view.
        # If there is no ScrollView, the user will not be able to see list
        # items that are outside of the screen.
        self.scroll_view = ScrollView()

        # Movies are put in the movies_list
        # (the movie_list is put in the scroll_view, this is realized in the
        # `load_movies_list` method)

        # Search field and scroll view are put into the layout
        self.layout.add_widget(self.search_field)
        self.layout.add_widget(self.scroll_view)

        # And the layout is put into this screen
        self.add_widget(self.layout)
        self.add_widget(add_movie_button)

    def spinner_toggle(self):
        if not self.spinner.active:
            self.layout.add_widget(self.spinner)
            self.spinner.active = True
        else:
            self.layout.remove_widget(self.spinner)
            self.spinner.active = False

    def load_movies_list(self, movies):
        """ Method that loads list of movies to the screen.

        Separate method for loading the list is needed because when
        the movie is
        deleted from the list, or when the user types something in searchbar,
        the list should be reloaded
        """
        self.spinner_toggle()
        # Clear all elements in the scroll view
        # (this elements are movies list items)
        self.scroll_view.clear_widgets()

        self.movies = movies
        # List will contain all movies
        mdlist = MDList()

        # Add movies to the list one by one
        for movie in self.movies:
            list_item_widget = MovieListItem(movie)
            mdlist.add_widget(list_item_widget)

        self.spinner_toggle()
        # Add list to the scroll view
        self.scroll_view.add_widget(mdlist)

    def open_movie_adder_screen(self, touch):
        """Called when the user taps on the button and releases it"""
        MoviesTab.screens["movie_adder"].load_content()
        MoviesTab.screen_manager.transition.direction = "left"
        MoviesTab.screen_manager.switch_to(MoviesTab.screens["movie_adder"])


class MoviesTab(MDBottomNavigationItem):
    """Tab that contains all elements related to movies (from the lab task).

    It contains the screen with movies list and the search bar. If you tap on
    the list item, it will open it in another screen with detailed information.
    Also this class contains screen_manager and screens fields as static fields
    because access to this fields is needed from different parts of
    the application.
    """

    screen_manager = None
    screens = None

    def __init__(self, **kwargs):
        # Giving main text and icon to this tab
        super().__init__(name="movies", text="Movies",
                         icon="movie-multiple", **kwargs)

        # Screen manager is needed for switching between the screen with movies
        # list and the screen with detailed information about choosen movie.
        MoviesTab.screen_manager = ScreenManager()
        # Here are created two screens that is used in MovieTab.
        MoviesTab.screens = {
            "movies_list": MoviesListScreen(name="movies_list"),
            "movie_info": MovieInfoScreen(name="movie_info"),
            "movie_adder": MovieAdderScreen(name="movie_adder")
        }

        # Put created screens into Screen Manager.
        for screen in self.screens.values():
            MoviesTab.screen_manager.add_widget(screen)

        # Put the screen manager into the our tab with movies.
        self.add_widget(MoviesTab.screen_manager)
