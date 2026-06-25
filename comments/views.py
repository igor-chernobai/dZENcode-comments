from rest_framework import filters, generics

from comments.models import Comment
from comments.serializers import CommentSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(parent=None)
    serializer_class = CommentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email', 'created_at']
    ordering = ['-created_at']
