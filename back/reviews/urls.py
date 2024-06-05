from django.urls import path
from . import views

urlpatterns = [
    path('', views.review_list),
    path('<int:reviwe_pk>/', views.review_detail),
    path('delete/<int:review_id>/', views.review_delete)
]
