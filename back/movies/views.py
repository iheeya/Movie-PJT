from django.http import JsonResponse
from .models import Movie, Actor, Director, Genre
import requests

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
# from rest_framework.decorators import permission_classes
# from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import MovieListSerializer, MovieActorsSerializer, MovieDirectorSerializer, MovieGenresSerializer
from .models import Movie

def get_genre_name_by_id(genre_id):
    genre_map = {
        28: 'Action',
        12: 'Adventure',
        16: 'Animation',
        35: 'Comedy',
        80: 'Crime',
        99: 'Documentary',
        18: 'Drama',
        10751: 'Family',
        14: 'Fantasy',
        36: 'History',
        27: 'Horror',
        10402: 'Music',
        9648: 'Mystery',
        10749: 'Romance',
        878: 'Science Fiction',
        10770: 'TV Movie',
        53: 'Thriller',
        10752: 'War',
        37: 'Western'
    }
    return genre_map.get(genre_id, 'Unknown')

# 영화 데이터 받아오기
def fetch_movie_data(request):
    for page in range(1, 11):  # 1페이지부터 10페이지까지
        url = f"https://api.themoviedb.org/3/movie/popular?page={page}&language=ko-KR"
        headers = {
            "accept": "application/json",
            "Authorization": "Bearer #"  # 여기에 본인의 API 키를 입력하세요
        }
        response = requests.get(url, headers=headers)
        data = response.json()
        print('movies data = ', data)
        results = data.get('results')
        for movie_data in results:
            # Create a Movie object and save it to the database
            movie = Movie.objects.create(
                movie_id=movie_data.get('id',''),
                title=movie_data.get('title', ''),
                overview=movie_data.get('overview', ''),
                release_date=movie_data.get('release_date', ''),
                vote_average=movie_data.get('vote_average', 0),          
                poster_path=movie_data.get('poster_path', ''),   
            )
            
            genre_ids = movie_data.get('genre_ids', [])
            genres = []
            for genre_id in genre_ids:
                genre_name = get_genre_name_by_id(genre_id)
                genre, created = Genre.objects.get_or_create(name=genre_name)
                genres.append(genre)
            
            # set 메소드를 사용하여 다대다 관계 설정
            movie.genres.set(genres)
            
            # 영화의 크레딧 정보 가져오기
            credit_url = f"https://api.themoviedb.org/3/movie/{movie.movie_id}/credits?language=ko-KR"
            credit_response = requests.get(credit_url, headers=headers)
            credit_data = credit_response.json()
            
            # 감독 정보 저장
            directors = []
            for crew_member in credit_data.get('crew', []):
                if crew_member['job'] == 'Director':
                    director, _ = Director.objects.get_or_create(name=crew_member['name'])
                    directors.append(director)
            movie.directors.set(directors)

            # 배우 정보 저장
            actors = []
            for cast_member in credit_data.get('cast', []):
                actor, _ = Actor.objects.get_or_create(name=cast_member['name'])
                actors.append(actor)
            movie.actors.set(actors)
            
            
            movie.save()
            
            print(movie_data.get('title', ''))
    return JsonResponse({"msg": f"{results}"})


@api_view(['GET'])
def movie_list(request):
    if request.method == 'GET':
        # 영화 리스트
        movies = get_list_or_404(Movie)
        movie_serializer = MovieListSerializer(movies, many=True)
        
        return Response(movie_serializer.data)


@api_view(['GET'])
def movie_gnere(request):
    if request.method == 'GET':
        # 영화 리스트
        genres = get_list_or_404(Genre)
        genres_serializer = MovieGenresSerializer(genres, many=True)
        
        return Response(genres_serializer.data)

    
# # 4개의 모델, 시리얼라이저 한번에 응답 보내기
# @api_view(['GET'])
# def movie_list(request):
#     if request.method == 'GET':
#         # 영화 리스트
#         movies = get_list_or_404(Movie)
#         movie_serializer = MovieListSerializer(movies[:50], many=True)
        
#         # 장르 리스트
#         genres = get_list_or_404(Genre)
#         genre_serializer = MovieGenresSerializer(genres, many=True)
        
#         # 배우 리스트
#         actors = get_list_or_404(Actor)
#         actor_serializer = MovieActorsSerializer(actors, many=True)
        
#         # 감독 리스트
#         directors = get_list_or_404(Director)
#         director_serializer = MovieDirectorSerializer(directors, many=True)
        
#         # 응답 데이터 합치기
#         combined_data = {
#             'movies': movie_serializer.data,
#             'genres': genre_serializer.data,
#             'actors': actor_serializer.data,
#             'directors': director_serializer.data,
#         }
        
#         return Response(combined_data)



