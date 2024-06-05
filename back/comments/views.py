# Create your views here.
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import CommentListSerializer
from .models import Comment


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def comment_list(request):
    if request.method == 'GET':
        comments = get_list_or_404(Comment)
        serializer = CommentListSerializer(comments, many=True)
        return Response(serializer.data)
    
    elif request.method == 'POST':
        print("User:", request.user)
        print("Is authenticated:", request.user.is_authenticated)
        print("Request data:", request.data)

        if request.user.is_authenticated:
            serializer = CommentListSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                # serializer.save()
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "로그인이 되어 있지 않아요!"}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['DELETE'])
def comment_delete(request, comment_id):
    # comment_id를 통해 해당 댓글을 가져오기
    comment = get_object_or_404(Comment, id=comment_id)
    # 댓글 삭제
    comment.delete()
    return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)