from kinopoisk.movie import Movie


def format_movies(movies_list):
    return [f'{name} {year}' for name, year in zip(movies_list[0::2], movies_list[1::2])]


class MovieList:
    def __init__(self, name):
        self.name = name
        self.movies = Movie.objects.search(self.name)


class Film:
    def __init__(self, name):
        self.name = name
        self.id = Movie.objects.search(self.name)[0].id
        self.plot = None
        self.genres = None
        self.rating = None
        self.imdb = None

    def search_film(self):
        movie_list = Movie.objects.search(self.name)
        return movie_list

    def get_movie_content(self):
        movie = Movie(self.id)
        movie.get_content('main_page')
        self.plot = movie.plot
        self.genres = movie.genres
        self.rating = movie.rating
        # self.imdb = movie.imdb
