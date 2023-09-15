from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import UserDetail, UserList, UserViewSet

# urlpatterns = [
#     path("<int:pk>/", UserDetail.as_view(), name="user_detail"),
#     path("", UserList.as_view(), name="user_list"),
# ]

router = SimpleRouter()
router.register("", UserViewSet, basename="users")

urlpatterns = router.urls
