import json

from asgiref.sync import async_to_sync
from captcha.helpers import captcha_image_url
from captcha.models import CaptchaStore
from channels.layers import get_channel_layer
from django.core.cache import cache
from rest_framework import filters, generics
from rest_framework.response import Response
from rest_framework.views import APIView

from comments.models import Comment
from comments.serializers import CommentSerializer
from comments.tasks import resize_img


class CommentListCreateAPIView(generics.ListCreateAPIView):
    queryset = Comment.objects.filter(parent=None)
    serializer_class = CommentSerializer
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ['username', 'email', 'created_at']
    ordering = ['-created_at']
    authentication_classes = []

    def list(self, request, *args, **kwargs):
        key = f'comments:{request.get_full_path()}'
        data = cache.get(key)
        if data is None:
            response = super().list(request, *args, **kwargs)
            cache.set(key, response.data, 300)
            return response
        return Response(data)

    def perform_create(self, serializer):
        comment = serializer.save()

        if comment.image:
            resize_img.delay(comment.id)

        cache.clear()

        channel_layers = get_channel_layer()
        async_to_sync(channel_layers.group_send)(
            'comments', {'type': 'comment.message', 'message': json.dumps(CommentSerializer(comment).data)}
        )


class CaptchaAPIView(APIView):
    def get(self, request):
        key = CaptchaStore.generate_key()
        return Response({'key': key, 'image_url': captcha_image_url(key)})
