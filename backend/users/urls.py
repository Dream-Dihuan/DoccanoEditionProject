from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import Me, UserCreation, Users, UserViewSet

# 创建路由器并注册视图集
router = DefaultRouter()
router.register(r'external-users', UserViewSet, basename='external-user')

urlpatterns = [
    path(route="me", view=Me.as_view(), name="me"),
    path(route="users", view=Users.as_view(), name="user_list"),
    path(route="users/create", view=UserCreation.as_view(), name="user_create"),
    path('external/', include(router.urls)),
    path("auth/", include("dj_rest_auth.urls")),
]