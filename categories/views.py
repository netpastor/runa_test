from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Category
from .serializers import CategoryCreateSerializer, CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    http_method_names = ("get", "post")
    permission_classes = (AllowAny,)
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def create(self, request, *args, **kwargs) -> Response:
        serializer = CategoryCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"success": True}, status=status.HTTP_201_CREATED)
