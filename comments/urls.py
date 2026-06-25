from django.urls import path

from comments import views

urlpatterns = [
    path('api/comments_list/', views.CommentListAPIView.as_view()),
]
