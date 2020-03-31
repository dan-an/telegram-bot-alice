from kinopoisk.movie import Movie


def format_movies(movies_list):
    return [f'{name} {year}' for name, year in zip(movies_list[0::2], movies_list[1::2])]


class MovieList:
    def __init__(self, search_name):
        self.movies = Movie.objects.search(search_name)


class Film:
    def __init__(self, film_id):
        self.id = film_id
        self.title = None
        self.plot = None
        self.genres = None
        self.rating_kp = None
        self.rating_imdb = None

    def search_film(self):
        movie_list = Movie.objects.search(self.name)
        return movie_list

    def get_movie_content(self):
        movie = Movie(self.id)
        movie.get_content('main_page')
        self.plot = movie.plot
        self.genres = movie.genres
        self.rating_kp = movie.rating
        self.title = movie.title
        self.rating_imdb = movie.imdb_rating
        self.year = movie.year
