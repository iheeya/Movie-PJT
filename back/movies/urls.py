from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('update_movie_database/', views.fetch_movie_data, name='update_movie_database'),
    path('movie_lists/', views.movie_list),
    path('genre_lists/', views.movie_gnere),
]