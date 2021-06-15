# import json
import requests
from urllib.parse import quote


class MoviesProvider:
    __slots__ = ()

    API_TOKEN = "ce5f874b2bf3fe1f5c508a9d84c8063a"
    URL = "https://api.themoviedb.org/3/search/movie/"
    DETAILED_INFO_URL = "https://api.themoviedb.org/3/movie/"

    @classmethod
    def find_movies(cls, query):
        filtered_query = quote(query)

        query_url = (
            f"{cls.URL}?api_key={cls.API_TOKEN}"
            f"&query={filtered_query}"
        )

        json_response = requests.get(query_url).json()

        movies = []
        for json_movie in json_response["results"]:
            movies.append(Movie(
                id_=json_movie["id"],
                title=json_movie["title"],
                poster_path=json_movie["poster_path"],
                vote_average=json_movie["vote_average"]
            ))
        return movies

    @classmethod
    def load_details(cls, ID):
        json_response = requests.get(
            f"{cls.DETAILED_INFO_URL}{ID}?api_key={cls.API_TOKEN}").json()
        return json_response


class Movie:
    def __init__(self, id_=None, title=None, poster_path=None,
                 vote_average=None):
        self.id_ = id_ or ""
        self.title = title or ""
        if poster_path:
            self.poster_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            self.poster_path = "data/default.png"
        self.vote_average = vote_average or ""
        self._details_loaded = False

    @property
    def details(self):
        if not self._details_loaded:
            details_dict = MoviesProvider.load_details(self.id_)
            if details_dict:
                self._details = self.MovieDetails(**details_dict)
            else:
                self._details = self.MovieDetails()
            self._details_loaded = True
        return self._details

    def reload_details(self):
        self._details_loaded = False

    class MovieDetails:
        def __init__(self, overview=None,
                     tagline=None, status=None, genres=None, **kwargs):
            self.overview = overview or ""
            self.tagline = tagline or ""
            self.status = status or ""
            if genres:
                self.genres = []
                for i in genres:
                    self.genres.append(i["name"])
                self.genres = ", ".join(self.genres)
            else:
                self.genres = ""
