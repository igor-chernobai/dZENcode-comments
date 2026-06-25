from django.urls import path

from comments import views

urlpatterns = [
    path('api/comments/', views.CommentListCreateAPIView.as_view()),
]
