from rest_framework import serializers
from .models import Movie, Genre, Actor, Director

class MovieGenresSerializer(serializers.ModelSerializer):
    class Meta:
        model=Genre
        fields='__all__'

class MovieActorsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Actor
        fields='__all__'

class MovieDirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Director
        fields='__all__'


class MovieListSerializer(serializers.ModelSerializer):
    genres = MovieGenresSerializer(many=True)
    actors = MovieActorsSerializer(many=True)
    directors = MovieDirectorSerializer(many=True)
    
    class Meta:
        model = Movie
        fields = ['id', 'title', 'movie_id', 'overview', 'poster_path', 'release_date', 'vote_average', 'genres', 'actors', 'directors']