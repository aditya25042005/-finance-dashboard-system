from django.http import JsonResponse
from jwt import ExpiredSignatureError, InvalidTokenError
from django.conf import settings
import jwt
from .models import User
class SessionAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.open_paths = {
            "/users/login/",
              "/api/schema/",
          "/api/docs/",
    "/api/redoc/",

            
            
          
       }
        self.open_prefixes = (
            "/admin/",
            "/api/schema/",
            "/api/docs/",
            "/api/redoc/",
        )
        
    def __call__(self, request):
        request.jwt_authenticated = False
       

       
        if request.path in self.open_paths or request.path.startswith(self.open_prefixes):
            return self.get_response(request)
           
        token = request.COOKIES.get("access_token")
        ##for demo and swagger purpose 
        if not token:
            auth_header = request.headers.get("Authorization")
            if auth_header and auth_header.startswith("Bearer "):
                token = auth_header.split(" ", 1)[1]

        

        if not token:
            return JsonResponse(
                {"error": "Authentication required. Please login again."},
                status=401
            )

        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

            username = payload.get("username")
            if not username:
                return JsonResponse(
                    {"error": "Invalid token payload."},
                    status=401
                )

            try:
               

                user = User.objects.get(username=username, is_active=True)
                
            except User.DoesNotExist:
                return JsonResponse(
                    {"error": "User not found or inactive."},
                    status=401
                )

            request.users = user
            request.jwt_authenticated = True
        
        except ExpiredSignatureError:
            response = JsonResponse(
                {"error": "Token expired. Please login again."},
                status=401
            )
            response.delete_cookie("access_token")
            return response

        except InvalidTokenError:
            response = JsonResponse(
                {"error": "Invalid token. Please login again."},
                status=401
            )
            response.delete_cookie("access_token")
            return response


        print(f"Authenticated user: {request.users.username}, Role: {request.users.role}")
        return self.get_response(request)