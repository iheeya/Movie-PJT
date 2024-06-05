from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Movie, User
from .serializers import MovieSerializer
from collections import Counter
from django.db.models import Count
from django.http import JsonResponse


User = get_user_model()

@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def toggle_follow(request, username):
    if request.user.is_authenticated:
        try:
            person = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        current_user = request.user
        if person != current_user:
            if current_user in person.followers.all():
                person.followers.remove(current_user)
                is_following = False
            else:
                person.followers.add(current_user)
                is_following = True
            return Response({'is_following': is_following}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"message": "로그인이 되어 있지 않아요!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def follow_status(request, username):
    if request.user.is_authenticated:
        try:
            person = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        current_user = request.user
        is_following = current_user in person.followers.all()
        followers_count = person.followers.count()  # 팔로워 수
        following_count = person.followings.count()  # 팔로잉 수
        return Response({
            'is_following': is_following,
            'followers_count': followers_count,
            'following_count': following_count,
        }, status=status.HTTP_200_OK)


# 좋아요 기능
@api_view(['POST'])
# @permission_classes([IsAuthenticated])
def toggle_like(request, movie_id):
    if request.user.is_authenticated:
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)

        current_user = request.user
        if current_user in movie.user_set.all():
            movie.user_set.remove(current_user)
            is_liked = False
        else:
            movie.user_set.add(current_user)
            is_liked = True

        return Response({'is_liked': is_liked}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "로그인이 되어 있지 않아요!"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def like_status(request, movie_id):
    if request.user.is_authenticated:
        try:
            movie = Movie.objects.get(id=movie_id)
        except Movie.DoesNotExist:
            return Response({"error": "Movie not found."}, status=status.HTTP_404_NOT_FOUND)

        current_user = request.user
        is_liked = current_user in movie.user_set.all()
        return Response({'is_liked': is_liked}, status=status.HTTP_200_OK)
    else:
        return Response({"message": "로그인이 되어 있지 않아요!"}, status=status.HTTP_400_BAD_REQUEST)


 ####################################################





def get_user_liked_genres(user):
    liked_movies = user.likes.all()
    genre_counts = Counter()
    for movie in liked_movies:
        for genre in movie.genres.all():
            genre_counts[genre.name] += 1
    return genre_counts

def get_top_genres(genre_counts, top_n=3):
    top_genres = genre_counts.most_common(top_n)
    return [genre for genre, count in top_genres]

def recommend_movies(user, top_n=3):
    genre_counts = get_user_liked_genres(user)
    top_genres = get_top_genres(genre_counts, top_n)
    
    liked_movies = user.likes.all()
    liked_movie_ids = liked_movies.values_list('movie_id', flat=True)
    
    recommended_movies = Movie.objects.filter(
        genres__name__in=top_genres,
        # id__in=liked_movie_ids,  # 수정된 부분
    ).exclude(
        id__in=liked_movie_ids
    ).exclude(
    user=user
    ).distinct().annotate(
        num_likes=Count('user')
    ).order_by('-num_likes')[:10]
    
    return recommended_movies

@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def recommend_movies_view(request):
    if request.user.is_authenticated:
        user = request.user
        recommended_movies = recommend_movies(user)
        serializer = MovieSerializer(recommended_movies, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response({"message": "사용자가 인증되지 않았습니다."}, status=status.HTTP_401_UNAUTHORIZED)






@api_view(['GET'])
def liked_movies_count(request):
    if request.user.is_authenticated:
        user = request.user
        liked_movies_count = user.likes.count()  # 좋아요를 누른 영화의 총 개수
        return JsonResponse({'liked_movies_count': liked_movies_count})
    else:
        # 사용자가 인증되지 않은 경우 401 Unauthorized 에러를 반환합니다.
        return JsonResponse({'error': 'User not authenticated.'}, status=401)
    
    
@api_view(['GET'])
def liked_movies_list(request):
    if request.user.is_authenticated:
        user = request.user
        # 현재 로그인한 사용자가 좋아요를 누른 영화들을 가져옵니다.
        liked_movies = user.likes.all()  # 이 부분은 실제 모델에 따라 다를 수 있습니다.

        # 각 영화의 정보를 적절한 형태로 가공합니다.
        movies_data = []
        for movie in liked_movies:
            movie_data = {
                'id': movie.id,
                'title': movie.title,
                'poster_path': movie.poster_path
                # 필요한 다른 정보들도 추가할 수 있습니다.
            }
            movies_data.append(movie_data)

        return JsonResponse({'movies': movies_data})


@api_view(['GET'])
def user_liked_movies(request, username):
    if request.user.is_authenticated:
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        liked_movies = user.likes.all()
        serializer = MovieSerializer(liked_movies, many=True)
        return Response(serializer.data)