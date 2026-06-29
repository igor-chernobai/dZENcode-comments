import json

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.cache import cache
from rest_framework import filters, generics
from rest_framework.response import Response

from comments.models import Comment
from comments.serializers import CommentSerializer
from comments.tasks import resize_img


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(parent=None)
    serializer_class = CommentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email', 'created_at']
    ordering = ['-created_at']

    def list(self, request):
        qs_cache = cache.get('comments_list')

        if qs_cache:
            qs = qs_cache
        else:
            qs = self.get_queryset()
            cache.set('comments_list', qs, 300)

        serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        comment = serializer.save()

        if comment.image:
            resize_img.delay(comment.id)

        cache.delete('comments_list')

        channel_layers = get_channel_layer()
        async_to_sync(channel_layers.group_send)(
            'comments', {'type': 'comment.message', 'message': json.dumps(CommentSerializer(comment).data)}
        )
