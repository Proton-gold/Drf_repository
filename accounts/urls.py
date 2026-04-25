from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenBlacklistView
from accounts.views import AuthViewSet
from task.views import TaskViewSet

router = DefaultRouter()
router.register('auth', AuthViewSet, basename='auth')
urlpatterns = [
    path('', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view()),
    path('api/token/refresh/', TokenRefreshView.as_view()),
    path('api/token/blacklist/', TokenBlacklistView.as_view()),

]
