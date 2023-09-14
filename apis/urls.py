from django.urls import path, include

urlpatterns = [
    path("posts/", include("posts.urls")),
    path("auth/", include("accounts.authentication.urls")),
]
