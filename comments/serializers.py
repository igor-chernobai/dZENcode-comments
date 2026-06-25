import re

import bleach
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

from comments.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    children = serializers.ListSerializer(child=RecursiveField(), read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'username', 'email', 'home_page', 'text', 'created_at', 'parent', 'file', 'image', 'children']

    def validate_username(self, value):
        if not re.match(r'^[a-zA-Z0-9]+$', value):
            raise serializers.ValidationError('Username must contain only Latin letters and numbers')

        return value

    def validate_file(self, value):
        if value and value.size > 102400:
            raise serializers.ValidationError('File cannot be bigger than 100kb')

        return value

    def validate_text(self, value):
        tags = {'a', 'code', 'i', 'strong'}
        attrs = {'a': ['title', 'href']}

        return bleach.clean(value, tags=tags, attributes=attrs, strip=True)
