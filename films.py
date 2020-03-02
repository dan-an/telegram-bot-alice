from kinopoisk.movie import Movie

class Film():
  def __init__(self, name):
    self.name = name
    self.id = Movie.objects.search(self.name)[0].id
    self.plot = None
    self.genres = None
    self.rating = None
    self.imdb = None

  def search_film(self):
    movie_list = Movie.objects.search(self.name)
    self.id = movie_list[0].id

  def get_movie_content(self):
    movie = Movie(self.id)
    movie.get_content('main_page')
    print(movie.get_content('main_page'))
    self.plot = movie.plot
    self.genres = movie.genres
    self.rating = movie.rating
    # self.imdb = movie.imdb
