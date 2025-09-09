from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserSerializer
from projects.permissions import IsProjectAdmin


class Me(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)


class Users(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated & IsProjectAdmin]
    pagination_class = None
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("username",)


class UserCreation(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [IsAuthenticated & IsAdminUser]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        user = serializer.save(self.request)
        return user


class UserViewSet(viewsets.ModelViewSet):
    """
    外部用户管理接口，支持增删改查操作
    
    提供完整的用户管理功能，包括：
    - 用户列表获取
    - 用户创建
    - 用户详情获取
    - 用户信息更新
    - 用户删除
    
    注意：此接口无需认证和权限验证，任何可以访问该接口的用户都可以执行所有操作。
    请确保该接口只能在受信任的网络环境中访问。
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ("username",)
    
    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action == 'list':
            # 列表操作需要项目管理员权限或超级用户权限
            permission_classes = [IsAuthenticated & (IsProjectAdmin | IsAdminUser)]
        else:
            # 其他操作需要超级用户权限
            permission_classes = [IsAuthenticated & IsAdminUser]
        return [permission() for permission in permission_classes]