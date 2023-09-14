from django.urls import path
from rest_framework.routers import SimpleRouter

from .views import PostViewSet, PostDetail, PostList

urlpatterns = [
    path("<int:pk>/", PostDetail.as_view(), name="post_detail"),
    path("", PostList.as_view(), name="post_list"),
]

# router = SimpleRouter()
# router.register("", PostViewSet, basename="posts")

# urlpatterns = router.urls
