'''
'''

# Import modules:

import traceback
from datetime import datetime
from functools import wraps
from flask import request, current_app as c_app
from utils.common_functions import get_token_fields
from redis_rate_limit import RateLimit, TooManyRequests

# Decorator Functions:

META = {
    'version': 1.1,
    "utc_timestamp": datetime.utcnow().isoformat(),
    "ist_timestamp": datetime.now().isoformat()
}
HEADERS = {'Content-Type': 'application/json'}
SUCCESS_CODE = 200
BAD_CODE = 400
AUTH_CODE = 401
FORBIDDEN_CODE = 403
PROCESS_ERROR_CODE = 422
RATE_LIMIT_CODE = 429
EXCEPTION_CODE = 500

def check_args(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            print({
                "url": request.base_url, "url_params": request.args.to_dict(),
                "headers": dict(request.headers), "timestamp": META.get('utc_timestamp'),
                "remote_ip": request.headers.get('X-Forwarded-For', request.remote_addr)
            })
            if request.path != '/v1/welcome' and request.args.to_dict() == {}:
                    response = {
                        'message': 'unable to process request',
                        'reason': 'url argument/s cannot be empty'
                    }
                    return response, BAD_CODE, HEADERS
            response = func(*args,**kwargs)
            return response

        except Exception as e:
            print(f'Exception while running function {func.__name__} as {e}')
            raise Exception
    return wrapper

def check_json(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            print({
                "url": request.base_url, "post_body": request.get_json(),
                "headers": dict(request.headers), "timestamp": META.get('utc_timestamp'),
                "remote_ip": request.headers.get('X-Forwarded-For', request.remote_addr)
            })
            if request.get_json() == {}:
                response = {
                    'message': 'unable to process request',
                    'reason': 'post body cannot be empty'
                }
                return response, BAD_CODE, HEADERS
            response = func(*args,**kwargs)
            return response

        except Exception as e:
            print(f'Exception while running function {func.__name__} as {e}')
            raise Exception
    return wrapper

def check_auth(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            if request.headers.get('Authorization') == None:
                response = {
                    'message': 'unable to process request',
                    'reason': 'Authorization header is missing'
                }
                return response, AUTH_CODE, HEADERS

            auth_token = request.headers.get("Authorization")
            token_fields = get_token_fields(auth_token)

            if "error" in token_fields:
                response = {
                    'message': 'unable to process request',
                    'reason': token_fields.get('error')
                }
                return response, AUTH_CODE, HEADERS

            response = func(*args,**kwargs)
            return response

        except Exception as e:
            print(f'Exception while running function {func.__name__} as {e}')
            raise Exception
    return wrapper

def check_super_auth(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            if request.headers.get('Authorization') == None:
                response = {
                    'message': 'unable to process request',
                    'reason': 'Authorization header is missing'
                }
                return response, AUTH_CODE, HEADERS

            auth_token = request.headers.get("Authorization")
            secret_key = c_app.config.get('SECRET_KEY')
            if auth_token != secret_key:
                response = {
                    'message': 'unable to process request',
                    'reason': 'Authorization header is incorrect'
                }
                return response, AUTH_CODE, HEADERS

            response = func(*args,**kwargs)
            return response
        except Exception as e:
            print(f'Exception while running function {func.__name__} as {e}')
            raise Exception
    return wrapper

def handle_exception(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            response = func(*args,**kwargs)
            return response
        except Exception as e:
            print(f'Exception while running function {func.__name__} as {e}')
            raise Exception
    return wrapper

def retry_on_exception(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        for i in range(5):
            try:
                response = func(*args, **kwargs)
                return response
            except Exception as e:
                print(f'Exception while running function {func.__name__} as {e}, retrying ... {i+1}')
                time.sleep(1)
    return wrapper

def rate_limit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            client = request.headers.get('X-Forwarded-For', request.remote_addr)
            max_requests = c_app.config.get('API_RATE_LIMITS').get(request.path, 1)

            print(f'middleware.py: max_requests: {max_requests}')
            with RateLimit(
                resource='users_list', client=client, 
                max_requests=max_requests, expire=1, 
                redis_pool=c_app.config.get('REDIS_POOL')
            ):
                response = func(*args, **kwargs)
                return response

        except TooManyRequests:
            response = {
                "status": "failed",
                "message": "rate limit exceeded, try after some time"
            }
            return response, RATE_LIMIT_CODE, HEADERS

        except Exception as e:
            traceback.print_exc()
            print(f'Exception while running function {func.__name__} as {e}')
    return wrapper