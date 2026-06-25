from rest_framework import generics

from comments.models import Comment
from comments.serializers import CommentSerializer


class CommentListAPIView(generics.ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
