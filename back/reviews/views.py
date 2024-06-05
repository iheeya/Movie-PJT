from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

# permission Decorators
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404, get_list_or_404

from .serializers import ReviewListSerializer, ReviewSerailizer
from .models import Reivew


@api_view(['GET', 'POST'])
# @permission_classes([IsAuthenticated])
def review_list(request):
    if request.method == 'GET':
        reviews = get_list_or_404(Reivew)
        serializer = ReviewListSerializer(reviews, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        if request.user.is_authenticated:
            serializer = ReviewListSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                # serializer.save()
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"message": "로그인이 되어 있지 않아요!"}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def review_detail(request, review_pk):
    reviews= get_object_or_404(Reivew, pk=review_pk)

    if request.method == 'GET':
        serializer = ReviewSerailizer(reviews)
        print(serializer.data)
        return Response(serializer.data)
    
    
@api_view(['DELETE'])
def review_delete(request, review_id):
    review = get_object_or_404(Reivew, id=review_id)
    review.delete()
    return Response({"message": "Comment deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


