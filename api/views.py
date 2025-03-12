from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Post

from .serializers import PostSerializer

@api_view()
def test(request):
    return Response({'message': 'hello!'})


@api_view()
def posts(request):

    # получили посты из базы  данных
    posts = Post.objects.all()
    # передали все посты сериалазеру
    serializer = PostSerializer(posts, many=True)

    return Response(serializer.data)





