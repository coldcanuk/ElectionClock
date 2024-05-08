# auth.py
import os
from functools import wraps
from flask import request, jsonify

# Retrieve the AUTHME value
AUTHME = os.getenv('AUTHME')

def require_auth(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token != f"Bearer {AUTHME}":
            return jsonify({"error": "Unauthorized access"}), 401
        return func(*args, **kwargs)
    return decorated_function