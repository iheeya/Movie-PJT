from rest_framework import serializers
from .models import Reivew


class ReviewListSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Reivew
        fields = ('id', 'title', 'content', 'movie', 'user', 'score',)


class ReviewSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Reivew
        fields = '__all__'
        read_only_fields = ('user',)
