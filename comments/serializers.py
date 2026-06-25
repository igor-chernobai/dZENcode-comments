from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    children = serializers.ListSerializer(child=RecursiveField())

    class Meta:
        model = Comment
        fields = ['id', 'username', 'email', 'home_page', 'text', 'created_at', 'parent', 'file', 'image', 'children']
