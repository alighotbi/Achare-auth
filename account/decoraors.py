from functools import wraps
from django.core.cache import cache
from rest_framework.response import Response
from rest_framework import status

from .utils import get_client_ip

def ip_rate_limit(view_type='login', limit=3, timeout=3600):
     """
    Decorator to limit requests per IP using Django's cache.
    - view_type: 'login', 'otp', etc.
    - limit: max number of requests allowed
    - timeout: in seconds (default = 1 hour)
    """
    
     def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
           ip = get_client_ip(request)
           cache_key = f"{view_type}_attempts_{ip}"
           attempts = cache.get(cache_key, 0)
           
           if attempts >= limit:
               return Response(
                  {"message": f"Too many {view_type} attempts. Please try again later."},
                  status=status.HTTP_429_TOO_MANY_REQUESTS
               )
           
           response = view_func(self, request, *args, **kwargs)
           if response is None:
              return Response(
                 {"message": "An error occurred processing your request."},
                 status=status.HTTP_500_INTERNAL_SERVER_ERROR
              )
           
         #  Only increment if the response is not successful (i.e. not 200 or 201)
           if response.status_code not in [200, 201]:
              cache.set(cache_key, attempts + 1, timeout)
           
           # Reset attempts on success
           if response.status_code in [200, 201]:
              cache.delete(cache_key)
              
           return response
        
        return _wrapped_view
     return decorator  
        