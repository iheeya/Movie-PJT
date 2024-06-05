from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.comment_list),
    path('delete/<int:comment_id>/', views.comment_delete)
]