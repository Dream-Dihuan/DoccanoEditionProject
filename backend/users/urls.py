from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import Me, UserCreation, Users, InternalUserViewSet

# 创建路由器并注册视图集
internal_router = DefaultRouter()
internal_router.register(r'users', InternalUserViewSet, basename='internal-user')

urlpatterns = [
    path(route="me", view=Me.as_view(), name="me"),
    path(route="users", view=Users.as_view(), name="user_list"),
    path(route="users/create", view=UserCreation.as_view(), name="user_create"),
    path("auth/", include("dj_rest_auth.urls")),
    # 内部用户管理接口，仅限具有dihuanKey的系统访问
    path("internal/", include(internal_router.urls)),  
]