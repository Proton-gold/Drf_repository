from rest_framework.routers import DefaultRouter

from accounts.views import AuthViewSet
from task.views import TaskViewSet

router = DefaultRouter()
router.register('auth',AuthViewSet,basename='auth')
urlpatterns = router.urls