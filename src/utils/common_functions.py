"""
"""

# Import Modules:

from random import randint
from datetime import datetime, date, timedelta
import decimal
import time
import json
import secrets
import urllib.parse
import jwt
import requests
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError
from flask import current_app as c_app

def format_api_error(error):
    '''
    '''
    try:
        errors = {}
        for k, v in error.items():
            if isinstance(v, list):
                errors[k] = v[0]

            elif isinstance(v, dict):
                for k1, v1 in v.items():
                    if isinstance(v1, dict):
                        print(k1, v1)
                        for k2, v2 in v1.items():
                            # errors[f'{k} - {k1}'] = f'{k2} - {v2[0]}'
                            errors[f'{k} index {k1+1}'] = f'{k2} - {v2[0]}'
                    else:
                        errors[f'{k} - {k1}'] = v1

            elif isinstance(v, str):
                errors[k] = v
        return errors

    except Exception as e:
            raise e

def deserializer(objects):
    '''
    '''
    try:
        response = []
        for object in objects:
            d = {}
            for k, v in object.items():
                # print(k, type(v))
                if type(v) in [list, dict]:
                    d[k] = json.dumps(v)
                elif isinstance(v, date):
                    d[k] = v.isoformat()
                elif isinstance(v, timedelta):
                    d[k] = str(v)
                elif isinstance(v, decimal.Decimal):
                    d[k] = float(v)
                else:
                    d[k] = v

            if d is not None:
                response.append(d)
        return response

    except Exception as e:
        raise e

def get_token_fields(token):
    '''
    '''
    try:
        key = c_app.config.get('SECRET_KEY', 'qwertyuiopasdfghjklzxcvbnm123456')
        token_fields = jwt.decode(token, key, algorithms="HS256")
        return token_fields

    except ExpiredSignatureError as e:
        print(f"Expired Signature auth token: {token}")
        return {"error": "expired signature auth token"}

    except InvalidSignatureError as e:
        print(f"Invalid Signature auth token: {token}")
        return {"error": "invalid signature auth token"}

    except Exception as e:
        print(f"Token decode exception: {e}")
        return {"error": "token decode exception"}

    return {}        