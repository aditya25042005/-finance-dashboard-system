from django.http import JsonResponse

class SessionAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.open_paths = {
            "/users/login/",
           "/users/create/",
           
        }

    def __call__(self, request):
       
        if request.path in self.open_paths:
           
            return self.get_response(request)

        if not request.user.is_authenticated:

            return JsonResponse(
                {"error": "Session expired or authentication required."},
                status=401
            )

        return self.get_response(request)