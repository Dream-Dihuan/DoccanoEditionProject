from dj_rest_auth.registration.serializers import RegisterSerializer
from django.contrib.auth.models import User
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, generics, status, permissions
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .serializers import UserSerializer
from projects.permissions import IsProjectAdmin


class HasDihuanKey(permissions.BasePermission):
    """
    自定义权限类，只允许请求头中包含dihuanKey: dihuan的请求访问
    """

    def has_permission(self, request, view):
        dihuan_key = request.META.get('HTTP_DIHUANKEY')
        return dihuan_key == 'dihuan'


class Me(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, context={"request": request})
        return Response(serializer.data)


class InternalUserViewSet(ModelViewSet):
    """
    内部用户管理接口，提供完整的增删改查功能
    
    该视图集提供标准的RESTful API端点用于管理用户，只能通过在请求头中
    包含'dihuanKey: dihuan'来访问。
    
    标准端点:
    - GET /v1/internal/users/ - 获取用户列表
    - POST /v1/internal/users/ - 创建新用户
    - GET /v1/internal/users/{id}/ - 获取特定用户信息
    - PUT /v1/internal/users/{id}/ - 更新特定用户信息（全量更新）
    - PATCH /v1/internal/users/{id}/ - 部分更新特定用户信息
    - DELETE /v1/internal/users/{id}/ - 删除特定用户
    
    所有请求和响应的数据格式与现有用户API保持一致。
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [HasDihuanKey]

    def get_permissions(self):
        """
        实例化权限类
        """
        return [permission() for permission in self.permission_classes]


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