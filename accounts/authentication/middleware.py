import json
from rest_framework.parsers import JSONParser
from io import BytesIO
from django.utils.deprecation import MiddlewareMixin

from django_project.settings import REST_AUTH

JWT_AUTH_REFRESH_COOKIE = REST_AUTH["JWT_AUTH_REFRESH_COOKIE"]


class MoveJWTRefreshCookieIntoTheBody(MiddlewareMixin):
    """
    For Django Rest Framework JWT's POST "/logout/" endpoint. Check
    for a 'refresh' in the request.COOKIES and if there, move it to the body payload.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        self.process_request(request)
        response = self.get_response(request)
        return response

    def process_request(self, request):
        if "/logout/" in request.path and JWT_AUTH_REFRESH_COOKIE in request.COOKIES:
            jwt_refresh = request.COOKIES.get(JWT_AUTH_REFRESH_COOKIE)
            if jwt_refresh:
                # Assuming the request body is URL encoded,
                # You might need to adjust this if your request body is JSON or other formats
                request_body = request.body.decode("utf-8")

                # Check if the body is empty or not
                if request_body:
                    request_body += f"&refresh={jwt_refresh}"
                else:
                    request_body = f"refresh={jwt_refresh}"

                # Update the request body
                request._body = request_body.encode("utf-8")
            # if jwt_refresh:
            #     if hasattr(request, "_request"):
            #         stream = BytesIO(request._request.body)
            #         data = JSONParser().parse(stream)
            #     else:
            #         data = getattr(request, "data", {})

            #     data["refresh"] = jwt_refresh
            #     request.data = data
            #     print(request.data)
        #     data = {}
        #     data["refresh"] = request.COOKIES[JWT_AUTH_REFRESH_COOKIE]
        #     request._body = json.dumps(data).encode("utf-8")
        #     print(request.body)
        # return None
