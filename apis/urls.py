from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
)


urlpatterns = [
    path("posts/", include("posts.urls")),
    path("users/", include("accounts.urls")),
    path("auth/", include("accounts.auth.urls")),
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "schema/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
