from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.response import Response

from dj_rest_auth.views import LoginView, LogoutView
from dj_rest_auth.jwt_auth import get_refresh_view
from dj_rest_auth.registration.views import RegisterView
from allauth.account import app_settings as allauth_account_settings
from dj_rest_auth.app_settings import api_settings


from django_project import settings
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext_lazy as _

from django_project.settings import REST_AUTH

JWT_AUTH_REFRESH_COOKIE = REST_AUTH["JWT_AUTH_REFRESH_COOKIE"]


class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        # Modify the response to remove 'access' and 'refresh' fields
        if "access" in response.data and "refresh" in response.data:
            del response.data["access"]
            del response.data["refresh"]
        return response


def get_custom_refresh_view():
    """Returns a custom Token Refresh CBV based on the original one"""

    OriginalRefreshView = get_refresh_view()

    class CustomRefreshView(OriginalRefreshView):
        def finalize_response(self, request, response, *args, **kwargs):
            # Get the original behavior
            response = super().finalize_response(request, response, *args, **kwargs)

            # Modify the response data if necessary
            if response.status_code == status.HTTP_200_OK and (
                "access" in response.data or "refresh" in response.data
            ):
                response.data = {
                    "detail": "Successfully refreshed token",
                    "code": "token_valid",
                }
            return response

    return CustomRefreshView


class CustomRegisterView(RegisterView):
    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)

        # Modify the response to remove 'access' and 'refresh' fields
        if "access" in response.data and "refresh" in response.data:
            del response.data["access"]
            del response.data["refresh"]
        return response


class CustomLogoutView(LogoutView):
    def logout(self, request):
        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass
        if api_settings.SESSION_LOGIN:
            django_logout(request)

        response = Response(
            {"detail": _("Successfully logged out.")},
            status=status.HTTP_200_OK,
        )
        if api_settings.USE_JWT:
            # NOTE: this import occurs here rather than at the top level
            # because JWT support is optional, and if `USE_JWT` isn't
            # True we shouldn't need the dependency
            from rest_framework_simplejwt.exceptions import TokenError
            from rest_framework_simplejwt.tokens import RefreshToken

            from dj_rest_auth.jwt_auth import unset_jwt_cookies

            cookie_name = api_settings.JWT_AUTH_COOKIE

            unset_jwt_cookies(response)

            if "rest_framework_simplejwt.token_blacklist" in settings.INSTALLED_APPS:
                # add refresh token to blacklist
                try:
                    token = RefreshToken(request.COOKIES.get(JWT_AUTH_REFRESH_COOKIE))
                    token.blacklist()
                except KeyError:
                    response.data = {
                        "detail": _("Refresh token was not included in request data.")
                    }
                    response.status_code = status.HTTP_401_UNAUTHORIZED
                except (TokenError, AttributeError, TypeError) as error:
                    if hasattr(error, "args"):
                        if (
                            "Token is blacklisted" in error.args
                            or "Token is invalid or expired" in error.args
                        ):
                            response.data = {"detail": _(error.args[0])}
                            response.status_code = status.HTTP_401_UNAUTHORIZED
                        else:
                            response.data = {"detail": _("An error has occurred.")}
                            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

                    else:
                        response.data = {"detail": _("An error has occurred.")}
                        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            elif not cookie_name:
                message = _(
                    "Neither cookies or blacklist are enabled, so the token "
                    "has not been deleted server side. Please make sure the token is deleted client side.",
                )
                response.data = {"detail": message}
                response.status_code = status.HTTP_200_OK
        return response
