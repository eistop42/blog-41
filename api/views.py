from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import PostSerializer
from core.models import Post

@api_view()
def main(request):
    return Response({"message": "Hello, world!"})


@api_view()
def posts(request):

    serializer = PostSerializer(Post.objects.all(), many=True)

    return Response(serializer.data)