from django.urls import path
from . import views

urlpatterns = [
     path('follow/<str:username>/', views.toggle_follow),
     path('follow/<str:username>/status/', views.follow_status, name='follow-status'),
     path('movies/<int:movie_id>/toggle-like/', views.toggle_like),
     path('movies/<int:movie_id>/like-status/', views.like_status),
     path('recommendations/', views.recommend_movies_view, name='recommend-movies'),
     path('movie_like_count/', views.liked_movies_count), 
     path('liked_movies/', views.liked_movies_list), 
     path('profile/<str:username>/liked-movies/', views.user_liked_movies)
]