import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import filters, generics

from comments.models import Comment
from comments.serializers import CommentSerializer


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(parent=None)
    serializer_class = CommentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email', 'created_at']
    ordering = ['-created_at']

    def perform_create(self, serializer):
        comment = serializer.save()

        channel_layers = get_channel_layer()
        async_to_sync(channel_layers.group_send)(
            'comments', {'type': 'comment.message', 'message': json.dumps(CommentSerializer(comment).data)}
        )
