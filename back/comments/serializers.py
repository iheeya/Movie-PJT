from rest_framework import serializers
from .models import Comment

class CommentListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Comment
        fields = ('id', 'comment', 'user', 'review')