from kinopoisk.movie import Movie


class MovieList:
    def __init__(self, search_name):
        self.movies = Movie.objects.search(search_name)


class Film:
    def __init__(self, film_id):
        self.id = film_id
        self.title = None
        self.plot = None
        self.genres = None
        self.ratings = {
            'KP': None,
            'IMDB': None
        }
        self.year = None

    def get_movie_content(self):
        movie = Movie(self.id)
        movie.get_content('main_page')
        self.plot = movie.plot
        self.genres = movie.genres
        self.title = movie.title
        self.ratings['KP'] = movie.rating
        self.ratings['IMDB'] = movie.imdb_rating
        self.year = movie.year
