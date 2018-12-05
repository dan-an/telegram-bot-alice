from kinopoisk.movie import Movie

class Film():
  def __init__(self, name):
    self.name = name
    self.id = Movie.objects.search(self.name)[0].id
    self.plot = None
    self.genres = None

  def search_film(self):
    print(self.name)
    movie_list = Movie.objects.search(self.name)
    print(movie_list)
    self.id = movie_list[0].id

  def get_movie_content(self):
    movie = Movie(self.id)
    movie.get_content('main_page')
    self.plot = movie.plot
    self.genres = movie.genres