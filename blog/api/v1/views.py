from rest_framework.permissions import IsAuthenticatedOrReadOnly
from ...models import Post, Category
from .serializers import PostSerializer, CategorySerializer
from rest_framework import viewsets
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .paginations import DefaultPagination
from .filters import PostFilter

"""@api_view(["GET","POST"])
@permission_classes([IsAuthenticated])
def postlist(request):
    ''' V1 of post list view'''
    if request.method == "GET":
        posts = Post.objects.filter(status=True)
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
    elif request.method == "POST":
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)"""

# --------------------------------------------------------------------------------

"""class PostList(GenericAPIView):

    '''V2 of post list view'''

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

    def get(self,request):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many= True)
        return Response(serializer.data)
    
    
    def post(self,request):
        serializer = PostSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)"""

# --------------------------------------------------------------------------------------------

"""class PostList(GenericAPIView,mixins.ListModelMixin, mixins.CreateModelMixin ):

    '''V3 of post list view'''

    permission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)

    def get(self,request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    
    
    def post(self,request, *args, **kwargs):
        return self.create(request, *args, **kwargs)"""


# -----------------------------------------------------------------------------------------

"""class PostList(ListCreateAPIView):

    ''' V4 of Post list view'''
    
    permission_classes=[IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
"""
# -----------------------------------------------------------------------------------------

"""@api_view(["GET","PUT","DELETE"])
@permission_classes([IsAuthenticatedOrReadOnly])
def postdetail(request,id):

    '''V1 of Post detail view'''

    post= get_object_or_404(Post, pk=id, status=True)
    if request.method == "GET":
        serializer = PostSerializer(post)
        return Response(serializer.data)
    
    elif request.method == "PUT":
        serializer = PostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    elif request.method == "DELETE":
        post.delete()
        return Response({"detail":"Item removed successfully!"},status=status.HTTP_204_NO_CONTENT)"""

# ------------------------------------------------------------------------------------------------------------

"""class PostDetail(APIView):

    ''' V2 of post detail view''''

    premission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer

    def get (self, request, id):
        post= get_object_or_404(Post, pk=id, status=True)
        serializer = self.serializer_class(post)
        return Response(serializer.data)
    

    def put(self, request, id):
        post= get_object_or_404(Post, pk=id, status=True)
        serializer = PostSerializer(post, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
    
    def delete(self, request, id):
        post= get_object_or_404(Post, pk=id, status=True)
        post.delete()
        return Response({"detail":"Item removed successfully!"},status=status.HTTP_204_NO_CONTENT)"""

# ----------------------------------------------------------------------------------------------------------------------------

"""class PostDetail(GenericAPIView, mixins.RetrieveModelMixin,
                         mixins.UpdateModelMixin, mixins.DestroyModelMixin):
    '''V2 of post detail view'''
    premission_classes=[IsAuthenticatedOrReadOnly]
    serializer_class=PostSerializer
    queryset = Post.objects.filter(status=True)

    def get(self,request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)
    
    
    def put(self,request, *args, **kwargs):
        return self.update(request, *args, **kwargs)
    
    def delete(self,request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
"""

# ------------------------------------------------------------------------------------

"""class PostDetail(RetrieveUpdateDestroyAPIView):
    '''V3 of post detail view'''
    premission_classes=[IsAuthenticatedOrReadOnly]
    serializer_class=PostSerializer
    queryset = Post.objects.filter(status=True)"""

# --------------------------------------------------------------------------------------

"""class PostViewSet(viewsets.ViewSet):
    '''V1 of post view set'''
    premission_classes=[IsAuthenticatedOrReadOnly]
    serializer_class=PostSerializer
    queryset = Post.objects.filter(status=True)

    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, pk=None):
        post_object = get_object_or_404(self.queryset, pk=pk)
        serializer = self.serializer_class(post_object)
        return Response(serializer.data)
    
    def create(self, request, pk=None):
        pass

    def update(self, request, pk=None):
        pass

    def partial_update(self, request, pk=None):
        pass

    def destroy(self, request, pk=None):
        pass

"""
# ----------------------------------------------------------------------------------


class PostModelViewSet(viewsets.ModelViewSet):

    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.filter(status=True)
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    # filterset_fields = {"category":["exact","in"],
    #                     "author":["exact","in"],
    #                     "status":["exact","in"]}
    filterset_class = PostFilter

    search_fields = ["title", "content"]
    ordering_fields = ["published_date"]
    pagination_class = DefaultPagination


class CategoryModelViewSet(viewsets.ModelViewSet):

    premission_classes = [IsAuthenticatedOrReadOnly]
    serializer_class = CategorySerializer
    queryset = Category.objects.filter()
