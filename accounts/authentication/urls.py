from django.urls import path, include

from accounts.authentication.views import (
    CustomLoginView,
    CustomLogoutView,
    CustomRegisterView,
    get_custom_refresh_view,
)

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="rest_login"),
    path("logout/", CustomLogoutView.as_view(), name="rest_logout"),
    path(
        "token/refresh/",
        get_custom_refresh_view().as_view(),
        name="token_refresh",
    ),
    path("", include("dj_rest_auth.urls")),
    path("registration/", CustomRegisterView.as_view(), name="rest_register"),
    path("registration/", include("dj_rest_auth.registration.urls")),
]
